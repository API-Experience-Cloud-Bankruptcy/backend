from fastapi import HTTPException
from app.services.house_hunt import get_nearby_houses
from app.models.house_hunt import HouseFeatureCollection


class HouseHuntHandler:
    """房屋獵人 Handler"""

    async def get_nearby_houses(
        self, latitude: float, longitude: float, search_radius_km: float = 1.0
    ) -> HouseFeatureCollection:
        """
        取得指定座標附近的房屋資料

        Args:
            latitude: 緯度
            longitude: 經度
            search_radius_km: 搜索半徑（公里），預設 1.0 公里

        Returns:
            HouseFeatureCollection: GeoJSON 格式的房屋集合
        """
        result = await get_nearby_houses(latitude, longitude, search_radius_km)

        if not result.features:
            raise HTTPException(
                status_code=404,
                detail=f"在座標 ({latitude}, {longitude}) 半徑 {search_radius_km} 公里內查無房屋資料",
            )

        return result
