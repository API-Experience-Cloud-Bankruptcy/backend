import asyncio
import json
import sys
from pathlib import Path
import httpx

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


from app.models.chloride_Ionized_concrete import (
    ChlorideIonizedConcreteResponse,
    ChlorideIonizedConcreteFormatResponse,
    ChlorideIonizedConcreteItemFormat,
)
from data.util import get_geocode_from_arcgis

API_URL = "https://data.taipei/api/v1/dataset/15487e1f-a86e-4481-8ae9-3c331db5e3d4"


async def fetch_chloride_ionized_concrete() -> None:
    async with httpx.AsyncClient() as client:
        params = {"limit": 2000, "offset": 0, "scope": "resourceAquire"}
        response = await client.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        chloride_ionized_concrete_response = (
            ChlorideIonizedConcreteResponse.model_validate(data)
        )

        chloride_ionized_concrete_responses = []

        for item in chloride_ionized_concrete_response.result.results:
            code = item.county + item.building_location
            longitude, latitude = get_geocode_from_arcgis(code) or (0.0, 0.0)
            item_with_coords = ChlorideIonizedConcreteItemFormat(
                **item.model_dump(),
                longitude=longitude,
                latitude=latitude,
            )
            chloride_ionized_concrete_responses.append(item_with_coords)
            print(f"Processed: {item.building_name}")
            await asyncio.sleep(0.1)

        format_response = ChlorideIonizedConcreteFormatResponse(
            result=chloride_ionized_concrete_responses
        )

        with open(
            "data/chloride_ionized_concrete_format.json", "w", encoding="utf-8"
        ) as f:
            json.dump(
                format_response.model_dump(),
                f,
                ensure_ascii=False,
                indent=4,
            )


if __name__ == "__main__":
    asyncio.run(fetch_chloride_ionized_concrete())
