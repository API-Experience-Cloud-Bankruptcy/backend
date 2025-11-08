from app.models.chloride_ionized_concrete_geojson import (
    ChlorideIonizedConcreteFeatureCollection,
)
from app.services import chloride_ionized_concrete_geojson as service


class ChlorideIonizedConcreteGeoJSONHandler:
    """海砂屋建築物 GeoJSON Handler"""

    async def fetch_geojson(self) -> ChlorideIonizedConcreteFeatureCollection:
        """獲取所有海砂屋建築物的 GeoJSON 資料"""
        return await service.load_chloride_ionized_concrete_geojson()
