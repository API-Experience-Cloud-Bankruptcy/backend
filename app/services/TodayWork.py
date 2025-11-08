from app.models.todaywork import WorkFeatureCollection, WorkFeature
import httpx

API_URL = "https://tpnco.blob.core.windows.net/blobfs/Todaywork.json"


async def fetch_today_work() -> list[WorkFeature]:
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
        response.raise_for_status()
        data = response.json()
        col = WorkFeatureCollection.model_validate(data)
        return col.features
