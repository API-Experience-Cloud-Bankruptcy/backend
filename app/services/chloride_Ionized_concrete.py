import httpx
from app.models.chloride_Ionized_concrete import ChlorideIonizedConcreteResponse

API_URL = "https://data.taipei/api/v1/dataset/15487e1f-a86e-4481-8ae9-3c331db5e3d4"


async def fetch_chloride_ionized_concrete() -> ChlorideIonizedConcreteResponse:
    async with httpx.AsyncClient() as client:
        params = {"limit": 2000, "offset": 0, "scope": "resourceAquire"}
        response = await client.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        chloride_ionized_concrete_response = (
            ChlorideIonizedConcreteResponse.model_validate(data)
        )
        return chloride_ionized_concrete_response
