from app.models.todaywork import WorkFeatureCollection, WorkFeature
import httpx
import json

API_URL = "https://tpnco.blob.core.windows.net/blobfs/Todaywork.json"


async def fetch_today_work() -> list[WorkFeature]:
    async with httpx.AsyncClient(default_encoding="utf-8") as client:
        response = await client.get(API_URL)
        response.raise_for_status()
        raw_content = response.text

        if raw_content.startswith("\ufeff"):
            raw_content = raw_content[1:]

        cleaned_content = "".join(
            char
            for char in raw_content
            if char == "\n" or char == "\r" or ord(char) >= 32
        )

        try:
            data = json.loads(cleaned_content, strict=False)
        except json.JSONDecodeError as e:
            error_pos = e.pos if hasattr(e, "pos") else 0
            raise ValueError(
                f"Failed to parse JSON data at position {error_pos}"
            ) from e

        col = WorkFeatureCollection.model_validate(data)
        return col.features


if __name__ == "__main__":
    import asyncio

    features = asyncio.run(fetch_today_work())
    for feature in features:
        print(feature)
