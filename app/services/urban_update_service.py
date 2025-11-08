import json
import os
from typing import List, Tuple
from math import radians, sin, cos, sqrt, atan2
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.strtree import STRtree

from app.models.urban_update_model import (
    UrbanUpdateListResponse,
    UrbanUpdateResponse,
    UrbanRecord,
)

EARTH_RADIUS_KM = 6371.0


def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """使用 Haversine 公式計算兩點之間的距離（公里）"""
    lat1_rad, lat2_rad = radians(lat1), radians(lat2)
    delta_lat, delta_lon = radians(lat2 - lat1), radians(lon2 - lon1)

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
    )
    return EARTH_RADIUS_KM * 2 * atan2(sqrt(a), sqrt(1 - a))


def _create_polygon(coords) -> Polygon | MultiPolygon | None:
    """根據座標建立多邊形物件"""
    try:
        if not coords or not isinstance(coords, list):
            return None

        if len(coords) > 0 and isinstance(coords[0], list):
            if len(coords[0]) > 0 and isinstance(coords[0][0], list):
                if len(coords[0][0]) > 0 and isinstance(coords[0][0][0], list):
                    return MultiPolygon(coords)  # type: ignore
                else:
                    return Polygon(coords[0])  # type: ignore
        return None
    except Exception:
        return None


class UrbanUpdateService:
    def __init__(self):
        self.file_path = "public/urban-update.json"

    def load_data(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_urban_updates(self) -> UrbanUpdateListResponse:
        """取得所有都市更新資料"""
        data = self.load_data()
        responses = [
            UrbanUpdateResponse(
                status="success",
                districts=item.get("districts", "未知區"),
                records=item.get("records", []),
            )
            for item in data
        ]
        return UrbanUpdateListResponse(
            status="success" if data else "empty",
            data=responses,
        )

    def get_urban_update_by_district(self, district: str) -> UrbanUpdateResponse:
        """根據行政區取得都市更新資料"""
        data = self.load_data()

        for record in data:
            if record.get("districts") == district:
                return UrbanUpdateResponse(
                    status="success",
                    districts=record.get("districts", district),
                    records=record.get("records", []),
                )

        return UrbanUpdateResponse(
            status="empty",
            districts=district,
            records=[],
        )

    def search_nearby_updates(
        self, latitude: float, longitude: float, search_radius_km: float = 1.0
    ) -> List[Tuple[UrbanRecord, str, float]]:
        """
        搜索指定座標附近的都市更新案件

        Returns:
            List[Tuple[UrbanRecord, district, distance]]: (更新案件, 行政區, 距離) 的列表
        """
        data = self.load_data()
        search_point = Point(longitude, latitude)

        geometries = []
        record_map = {}  # {geom_index: (district, record_index)}

        for district_data in data:
            district = district_data.get("districts", "未知區")
            records = district_data.get("records", [])

            for record_idx, record in enumerate(records):
                coords = record.get("coordinates")
                if not coords:
                    continue

                polygon = _create_polygon(coords)
                if polygon:
                    geom_idx = len(geometries)
                    geometries.append(polygon)
                    record_map[geom_idx] = (district, record_idx, records)

        if not geometries:
            return []

        tree = STRtree(geometries)
        search_buffer = search_point.buffer(search_radius_km / 111.32)
        potential_indices = tree.query(search_buffer)

        results = []
        for geom_idx in potential_indices:
            geom_idx = int(geom_idx)
            polygon = geometries[geom_idx]
            district, record_idx, records = record_map[geom_idx]
            record_data = records[record_idx]

            if polygon.contains(search_point):
                distance_km = 0.0  # 點在多邊形內
            else:
                if polygon.geom_type == "Polygon":
                    nearest = polygon.exterior.interpolate(
                        polygon.exterior.project(search_point)
                    )
                    distance_km = _calculate_distance(
                        latitude, longitude, nearest.y, nearest.x
                    )
                elif polygon.geom_type == "MultiPolygon":
                    min_distance = float("inf")
                    for poly in polygon.geoms:
                        nearest = poly.exterior.interpolate(
                            poly.exterior.project(search_point)
                        )
                        dist = _calculate_distance(
                            latitude, longitude, nearest.y, nearest.x
                        )
                        min_distance = min(min_distance, dist)
                    distance_km = min_distance
                else:
                    continue

            if distance_km <= search_radius_km:
                urban_record = UrbanRecord(**record_data)
                results.append((urban_record, district, distance_km))

        return sorted(results, key=lambda x: x[2])

    def get_nearby_updates(
        self, latitude: float, longitude: float, search_radius_km: float = 1.0
    ) -> UrbanUpdateListResponse:
        """取得指定座標附近的都市更新資料,按行政區分組"""
        nearby = self.search_nearby_updates(latitude, longitude, search_radius_km)

        district_records = {}
        for record, district, _ in nearby:
            if district not in district_records:
                district_records[district] = []
            district_records[district].append(record)

        responses = [
            UrbanUpdateResponse(status="success", districts=district, records=records)
            for district, records in district_records.items()
        ]

        return UrbanUpdateListResponse(
            status="success" if responses else "empty", data=responses
        )


if __name__ == "__main__":
    service = UrbanUpdateService()
    updates = service.get_urban_update_by_district("大安區")
    count = len(updates.records)
    print(f"Found {count} updates for 大安區")
