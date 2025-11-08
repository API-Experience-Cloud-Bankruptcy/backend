from app.models.todaywork import WorkFeatureCollection
from app.services.TodayWork import fetch_today_work, get_nearby_features


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

    async def fetch_work_nearby(
        self,
        latitude: float,
        longitude: float,
        search_radius_km: float = 1.0
    ) -> WorkFeatureCollection:
        """
        取得指定座標附近的施工資料
        
        Args:
            latitude: 緯度
            longitude: 經度
            search_radius_km: 搜索半徑（公里），預設 1.0 公里
            
        Returns:
            WorkFeatureCollection: 包含附近施工資料的 FeatureCollection
        """
        return await get_nearby_features(latitude, longitude, search_radius_km)
