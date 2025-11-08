from app.models.earthquake_building_geojson import (
    EarthquakeBuildingFeatureCollection,
)
from app.services import earthquake_building_geojson as service


class EarthquakeBuildingGeoJSONHandler:
    """地震建築物 GeoJSON Handler"""

    async def fetch_geojson(self) -> EarthquakeBuildingFeatureCollection:
        """獲取所有地震建築物的 GeoJSON 資料"""
        return await service.load_earthquake_buildings_geojson()
