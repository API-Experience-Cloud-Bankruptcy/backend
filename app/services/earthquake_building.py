import httpx
from app.models.earthquakes_building import EarthquakeBuildingResponse

API_URL = "https://data.taipei/api/v1/dataset/a6e8f08e-ec2a-4be7-a762-54452b0c27df"


async def fetch_earthquake_buildings() -> EarthquakeBuildingResponse:
    async with httpx.AsyncClient() as client:
        params = {"limit": 2000, "offset": 0, "scope": "resourceAquire"}
        response = await client.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        earthquake_building_response = EarthquakeBuildingResponse.model_validate(data)
        return earthquake_building_response
