from app.models.todaywork import WorkFeatureCollection, WorkFeature
import httpx
import json
from shapely.geometry import Point, LineString, MultiLineString
from shapely.strtree import STRtree
from typing import List, Tuple
from math import radians, sin, cos, sqrt, atan2

API_URL = "https://tpnco.blob.core.windows.net/blobfs/Todaywork.json"
EARTH_RADIUS_KM = 6371.0


async def fetch_today_work() -> list[WorkFeature]:
    """取得今日施工資料"""
    async with httpx.AsyncClient(default_encoding="utf-8") as client:
        response = await client.get(API_URL)
        response.raise_for_status()

        raw_content = response.text.lstrip("\ufeff")
        cleaned_content = "".join(
            char for char in raw_content if char in "\n\r" or ord(char) >= 32
        )

        try:
            data = json.loads(cleaned_content, strict=False)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 解析失敗於位置 {getattr(e, 'pos', 0)}") from e

        return WorkFeatureCollection.from_wrong_format(data).features


def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """使用 Haversine 公式計算兩點之間的距離（公里）"""
    lat1_rad, lat2_rad = radians(lat1), radians(lat2)
    delta_lat, delta_lon = radians(lat2 - lat1), radians(lon2 - lon1)

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
    )
    return EARTH_RADIUS_KM * 2 * atan2(sqrt(a), sqrt(1 - a))


def _create_geometry(
    geom_type: str, coords
) -> Point | LineString | MultiLineString | None:
    try:
        if geom_type == "point" and isinstance(coords, list) and len(coords) >= 2:
            return Point(float(coords[0]), float(coords[1]))  # type: ignore
        elif geom_type == "linestring" and isinstance(coords, list):
            return LineString(coords)  # type: ignore
        elif geom_type == "multilinestring" and isinstance(coords, list):
            return MultiLineString(coords)  # type: ignore
    except Exception:
        pass
    return None


def _calculate_feature_distance(
    geom, search_point: Point, latitude: float, longitude: float
) -> float:
    if geom.geom_type == "Point":
        return _calculate_distance(latitude, longitude, geom.y, geom.x)
    else:
        nearest = geom.interpolate(geom.project(search_point))
        return _calculate_distance(latitude, longitude, nearest.y, nearest.x)


async def search_nearby_work(
    latitude: float, longitude: float, search_radius_km: float = 1.0
) -> List[Tuple[WorkFeature, float]]:
    """
    搜索指定座標附近的施工資料Ｆ
    """
    all_features = await fetch_today_work()
    search_point = Point(longitude, latitude)

    geometries = []
    feature_map = {}

    for idx, feature in enumerate(all_features):
        if not feature.geometry or not feature.geometry.coordinates:
            continue

        geom = _create_geometry(
            feature.geometry.type.lower(), feature.geometry.coordinates
        )

        if geom:
            geom_idx = len(geometries)
            geometries.append(geom)
            feature_map[geom_idx] = idx

    if not geometries:
        return []

    tree = STRtree(geometries)
    search_buffer = search_point.buffer(search_radius_km / 111.32)
    potential_indices = tree.query(search_buffer)

    results = []
    for geom_idx in potential_indices:
        geom_idx = int(geom_idx)
        geom = geometries[geom_idx]
        feature = all_features[feature_map[geom_idx]]

        distance_km = _calculate_feature_distance(
            geom, search_point, latitude, longitude
        )

        if distance_km <= search_radius_km:
            results.append((feature, distance_km))

    return sorted(results, key=lambda x: x[1])


async def get_nearby_features(
    latitude: float, longitude: float, search_radius_km: float = 1.0
) -> WorkFeatureCollection:
    nearby_results = await search_nearby_work(latitude, longitude, search_radius_km)
    features = [feature for feature, _ in nearby_results]

    return WorkFeatureCollection(type="FeatureCollection", features=features)
