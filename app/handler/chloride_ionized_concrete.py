from typing import List
from app.models.chloride_Ionized_concrete import (
    ChlorideIonizedConcreteResponse,
    ChlorideIonizedConcreteItem,
)
from app.services.chloride_Ionized_concrete import fetch_chloride_ionized_concrete


class ChlorideIonizedConcreteHandler:
    async def fetch_buildings(self) -> ChlorideIonizedConcreteResponse:
        """獲取所有海砂屋建築物資料"""
        return await fetch_chloride_ionized_concrete()

    async def fetch_buildings_by_county(
        self, county: str
    ) -> List[ChlorideIonizedConcreteItem]:
        """根據縣市別篩選海砂屋建築物"""
        all_data = await self.fetch_buildings()

        filtered_items = [
            item for item in all_data.result.results if item.county == county
        ]

        return filtered_items

    async def fetch_buildings_by_district(
        self, county: str, district: str
    ) -> List[ChlorideIonizedConcreteItem]:
        """根據縣市和行政區篩選海砂屋建築物"""
        all_data = await self.fetch_buildings()

        filtered_items = [
            item
            for item in all_data.result.results
            if item.county == county and item.district == district
        ]

        return filtered_items

    async def fetch_building_by_id(
        self, building_id: int
    ) -> ChlorideIonizedConcreteItem | None:
        """根據 ID 獲取特定海砂屋建築物"""
        all_data = await self.fetch_buildings()

        for item in all_data.result.results:
            if item.id == building_id:
                return item

        return None

    async def fetch_buildings_by_purpose(
        self, purpose: str
    ) -> List[ChlorideIonizedConcreteItem]:
        """根據使用目的篩選海砂屋建築物"""
        all_data = await self.fetch_buildings()

        filtered_items = [
            item for item in all_data.result.results if purpose in item.purpose
        ]

        return filtered_items

    async def fetch_buildings_by_organizer(
        self, organizer: str
    ) -> List[ChlorideIonizedConcreteItem]:
        """根據主辦單位篩選海砂屋建築物"""
        all_data = await self.fetch_buildings()

        filtered_items = [
            item for item in all_data.result.results if organizer in item.organizer
        ]

        return filtered_items
