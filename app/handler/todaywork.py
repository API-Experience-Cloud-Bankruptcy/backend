from app.models.todaywork import WorkFeatureCollection
from app.services.TodayWork import fetch_today_work


class TodayWorkHandler:
    async def fetch_work_data(self) -> WorkFeatureCollection:
        features = await fetch_today_work()
        return WorkFeatureCollection(type="FeatureCollection", features=features)

    async def fetch_work_by_district(self, district: str) -> WorkFeatureCollection:
        all_data = await self.fetch_work_data()

        filtered_features = [
            feature
            for feature in all_data.features
            if feature.properties.c_name == district
        ]

        return WorkFeatureCollection(
            type="FeatureCollection", features=filtered_features
        )

    async def fetch_work_by_contractor(self, contractor: str) -> WorkFeatureCollection:
        all_data = await self.fetch_work_data()

        filtered_features = [
            feature
            for feature in all_data.features
            if contractor in feature.properties.tc_na
        ]

        return WorkFeatureCollection(
            type="FeatureCollection", features=filtered_features
        )
