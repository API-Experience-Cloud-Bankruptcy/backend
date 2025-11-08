import httpx
from models.work_diagram import WorkProject, WorkProjectResponse

API_URL = (
    "https://data.taipei/api/v1/dataset/690fb291-77c0-484c-bbe8-d6babf45bc9b?scope=resourceAquire&limit=2000"
)


async def fetch_property_data() -> list[WorkProject]:
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
        response.raise_for_status()
        data = response.json()
        work_project_response = WorkProjectResponse.model_validate(data)
        return work_project_response.results
