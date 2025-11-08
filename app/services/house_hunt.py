import httpx
from typing import List, Tuple
from math import radians, sin, cos, sqrt, atan2
from shapely.geometry import Point
from shapely.strtree import STRtree
from app.models.house_hunt import (
    HouseRawData,
    HouseRawDataList,
    HouseFeatureCollection,
)

API_URL = "https://househunt.land.gov.taipei/app/communityList"
EARTH_RADIUS_KM = 6371.0


def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lat1_rad, lat2_rad = radians(lat1), radians(lat2)
    delta_lat, delta_lon = radians(lat2 - lat1), radians(lon2 - lon1)

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
    )
    return EARTH_RADIUS_KM * 2 * atan2(sqrt(a), sqrt(1 - a))


def _build_bounding_box(latitude: float, longitude: float, radius_km: float) -> str:
    """
    字串格式: "lon1 lat1,lon2 lat2,lon3 lat3,lon4 lat4,lon1 lat1"
    """

    lat_offset = radius_km / 111.32
    lon_offset = radius_km / (111.32 * cos(radians(latitude)))

    min_lon = longitude - lon_offset
    max_lon = longitude + lon_offset
    min_lat = latitude - lat_offset
    max_lat = latitude + lat_offset

    return (
        f"{min_lon} {min_lat},"
        f"{max_lon} {min_lat},"
        f"{max_lon} {max_lat},"
        f"{min_lon} {max_lat},"
        f"{min_lon} {min_lat}"
    )


async def fetch_house_hunt_raw(
    latitude: float,
    longitude: float,
    radius_km: float = 5.0,
    house_type: int = 0,
    page: str = "",
    builder_type: str = "",
    age: str = "",
    transaction_date: str = "",
    price_range: str = "",
) -> List[dict]:
    position = _build_bounding_box(latitude, longitude, radius_km)

    params = {
        "position": position,
        "type": house_type,
        "page": page,
        "radius": "",
        "builderType": builder_type,
        "age": age,
        "transactionDate": transaction_date,
        "priceRange": price_range,
    }

    async with httpx.AsyncClient(default_encoding="utf-8") as client:
        response = await client.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()


async def fetch_all_houses(
    latitude: float, longitude: float, radius_km: float = 5.0
) -> List[HouseRawData]:
    """取得所有房屋資料"""
    data = await fetch_house_hunt_raw(latitude, longitude, radius_km)

    houses = []
    for item in data:
        try:
            coords = item.get("geometry", {}).get("coordinates", [])
            if len(coords) >= 2:
                props = item.get("properties", {})

                house_data = {**props, "longitude": coords[0], "latitude": coords[1]}

                house = HouseRawData(**house_data)
                houses.append(house)
        except Exception:
            continue

    return houses


async def search_nearby_houses(
    latitude: float, longitude: float, search_radius_km: float = 1.0
) -> List[Tuple[HouseRawData, float]]:
    """
    搜索指定座標附近的房屋

    使用 Shapely STRtree 空間索引進行高效搜索

    Returns:
        List[Tuple[HouseRawData, float]]: (房屋資料, 距離) 的列表,按距離排序
    """

    all_houses = await fetch_all_houses(latitude, longitude, search_radius_km * 2)

    if not all_houses:
        return []

    search_point = Point(longitude, latitude)

    geometries = []
    house_map = {}

    for idx, house in enumerate(all_houses):
        point = Point(house.longitude, house.latitude)
        geom_idx = len(geometries)
        geometries.append(point)
        house_map[geom_idx] = idx

    tree = STRtree(geometries)
    search_buffer = search_point.buffer(search_radius_km / 111.32)
    potential_indices = tree.query(search_buffer)

    results = []
    for geom_idx in potential_indices:
        geom_idx = int(geom_idx)
        house_idx = house_map[geom_idx]
        house = all_houses[house_idx]

        distance_km = _calculate_distance(
            latitude, longitude, house.latitude, house.longitude
        )

        if distance_km <= search_radius_km:
            results.append((house, distance_km))

    return sorted(results, key=lambda x: x[1])


async def get_nearby_houses(
    latitude: float, longitude: float, search_radius_km: float = 1.0
) -> HouseFeatureCollection:
    nearby_results = await search_nearby_houses(latitude, longitude, search_radius_km)
    houses = [house for house, _ in nearby_results]

    house_list = HouseRawDataList(data=houses)
    return house_list.to_geojson()
