from typing import List
from app.models.earthquakes_building import (
    EarthquakeBuildingResponse,
    EarthquakeBuildingItem,
)
from app.services.earthquake_building import fetch_earthquake_buildings


class EarthquakeBuildingHandler:
    async def fetch_buildings(self) -> EarthquakeBuildingResponse:
        """獲取所有地震建築物資料"""
        return await fetch_earthquake_buildings()

    async def fetch_buildings_by_county(self, county: str) -> List[EarthquakeBuildingItem]:
        """根據縣市別篩選地震建築物"""
        all_data = await self.fetch_buildings()

        filtered_items = [
            item for item in all_data.result.results if item.county == county
        ]

        return filtered_items

    async def fetch_buildings_by_district(
        self, county: str, district: str
    ) -> List[EarthquakeBuildingItem]:
        """根據縣市和行政區篩選地震建築物"""
        all_data = await self.fetch_buildings()

        filtered_items = [
            item
            for item in all_data.result.results
            if item.county == county and item.district == district
        ]

        return filtered_items

    async def fetch_building_by_id(self, building_id: int) -> EarthquakeBuildingItem | None:
        """根據 ID 獲取特定地震建築物"""
        all_data = await self.fetch_buildings()

        for item in all_data.result.results:
            if item.id == building_id:
                return item

        return None
