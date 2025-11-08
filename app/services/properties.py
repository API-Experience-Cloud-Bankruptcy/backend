import httpx
from app.models.properties import FeatureCollection, Feature

API_URL = (
    "https://map.udd.gov.taipei/TaipeiDIS07/taipei/udd/map_redevelop_segment_10.json"
)


async def fetch_properties() -> list[Feature]:
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
        response.raise_for_status()
        data = response.json()
        feature_collection = FeatureCollection.model_validate(data)
        return feature_collection.features
