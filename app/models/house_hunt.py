from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class NearbyCommunity(BaseModel):
    """附近社區資訊"""

    community_name: str = Field(..., alias="communityName", description="社區名稱")
    price: str = Field(..., description="價格")
    history_low_price: str = Field(
        ..., alias="historyLowPrice", description="歷史最低價"
    )

    class Config:
        populate_by_name = True


class HouseProperties(BaseModel):
    """房屋屬性"""

    community_id: int = Field(..., alias="communityId", description="社區ID")
    community_name: str = Field(..., alias="communityName", description="社區名稱")
    now_average_price: str = Field(
        ..., alias="nowAveragePrice", description="目前平均價格"
    )
    now_average_price_is_car: bool = Field(
        ..., alias="nowAveragePriceIsCar", description="目前均價是否含車位"
    )
    history_height_price: str = Field(
        ..., alias="historyHeightPrice", description="歷史最高價"
    )
    history_height_price_is_car: str = Field(
        ..., alias="historyHeightPriceIsCar", description="歷史最高價是否含車位"
    )
    history_average_price: str = Field(
        ..., alias="historyAveragePrice", description="歷史平均價"
    )
    history_average_price_is_car: str = Field(
        ..., alias="historyAveragePriceIsCar", description="歷史均價是否含車位"
    )
    history_low_price: str = Field(
        ..., alias="historyLowPrice", description="歷史最低價"
    )
    history_low_price_is_car: str = Field(
        ..., alias="historyLowPriceIsCar", description="歷史最低價是否含車位"
    )
    buffer_zones_price: str = Field(
        ..., alias="bufferZonesPrice", description="緩衝區價格"
    )
    buffer_zones_price_is_car: bool = Field(
        ..., alias="bufferZonesPriceIsCar", description="緩衝區價格是否含車位"
    )
    architecture_type: int = Field(
        ..., alias="architectureType", description="建築類型"
    )
    housing_total_number: str = Field(
        ..., alias="housingTotalNumber", description="總戶數"
    )
    age: int = Field(..., description="屋齡")
    average_price: float = Field(..., alias="averagePrice", description="平均價格")
    average_square_feet: float = Field(
        ..., alias="averageSquareFeet", description="平均坪數"
    )
    house_number: str = Field(..., alias="houseNumber", description="門牌號碼")
    building_material: str = Field(..., alias="buildingMaterial", description="建材")
    use_type: str = Field(..., alias="useType", description="使用分區")
    use_partition: str = Field(..., alias="usePartition", description="使用分區類型")
    area: str = Field(..., description="面積")
    nearby_community: List[NearbyCommunity] = Field(
        ..., alias="nearbyCommunity", description="附近社區"
    )
    house_type: int = Field(..., alias="houseType", description="房屋類型")
    administrative_name: str = Field(
        ..., alias="administrativeName", description="行政區名稱"
    )
    totfloor: str = Field(..., description="總樓層")
    located: str = Field(..., description="地段")
    contract_download: List = Field(
        ..., alias="ContractDownload", description="合約下載"
    )
    performance_guarantee: str = Field(
        ..., alias="performanceGuarantee", description="履約保證"
    )
    project_director: Optional[str] = Field(
        None, alias="projectDirector", description="建案主任"
    )
    license: Optional[str] = Field(None, description="執照")
    presold_house_info: bool = Field(
        ..., alias="presoldHouseInfo", description="預售屋資訊"
    )
    good_community: bool = Field(..., alias="goodCommunity", description="優質社區")
    bank: str = Field(..., description="銀行")
    bank_link: str = Field(..., alias="bank_link", description="銀行連結")
    build_type: int = Field(..., alias="buildType", description="建物類型")
    avg_rent_last_year: str = Field(
        ..., alias="avg_rent_last_year", description="去年平均租金"
    )
    avg_rent_all_time: str = Field(
        ..., alias="avg_rent_all_time", description="歷史平均租金"
    )
    highest_rent_all_time: str = Field(
        ..., alias="highest_rent_all_time", description="歷史最高租金"
    )
    lowest_rent_all_time: str = Field(
        ..., alias="lowest_rent_all_time", description="歷史最低租金"
    )

    class Config:
        populate_by_name = True


class HouseGeometry(BaseModel):
    """房屋地理資訊"""

    type: Literal["Point"] = Field(..., description="幾何類型")
    coordinates: List[float] = Field(..., description="座標 [經度, 緯度]")


class HouseFeature(BaseModel):
    """房屋 Feature (GeoJSON 格式)"""

    type: Literal["Feature"] = Field(..., description="Feature 類型")
    geometry: HouseGeometry = Field(..., description="幾何資訊")
    properties: HouseProperties = Field(..., description="房屋屬性")


class HouseFeatureCollection(BaseModel):
    """房屋 FeatureCollection (GeoJSON 格式)"""

    type: Literal["FeatureCollection"] = Field(
        default="FeatureCollection", description="集合類型"
    )
    features: List[HouseFeature] = Field(..., description="房屋清單")


# ==================== 原始 API 格式 ====================


class HouseRawData(BaseModel):
    """原始 API 房屋資料格式"""

    community_id: int = Field(..., alias="communityId", description="社區ID")
    community_name: str = Field(..., alias="communityName", description="社區名稱")
    now_average_price: str = Field(
        ..., alias="nowAveragePrice", description="目前平均價格"
    )
    now_average_price_is_car: bool = Field(
        ..., alias="nowAveragePriceIsCar", description="目前均價是否含車位"
    )
    history_height_price: str = Field(
        ..., alias="historyHeightPrice", description="歷史最高價"
    )
    history_height_price_is_car: str = Field(
        ..., alias="historyHeightPriceIsCar", description="歷史最高價是否含車位"
    )
    history_average_price: str = Field(
        ..., alias="historyAveragePrice", description="歷史平均價"
    )
    history_average_price_is_car: str = Field(
        ..., alias="historyAveragePriceIsCar", description="歷史均價是否含車位"
    )
    history_low_price: str = Field(
        ..., alias="historyLowPrice", description="歷史最低價"
    )
    history_low_price_is_car: str = Field(
        ..., alias="historyLowPriceIsCar", description="歷史最低價是否含車位"
    )
    buffer_zones_price: str = Field(
        ..., alias="bufferZonesPrice", description="緩衝區價格"
    )
    buffer_zones_price_is_car: bool = Field(
        ..., alias="bufferZonesPriceIsCar", description="緩衝區價格是否含車位"
    )
    architecture_type: int = Field(
        ..., alias="architectureType", description="建築類型"
    )
    housing_total_number: str = Field(
        ..., alias="housingTotalNumber", description="總戶數"
    )
    age: int = Field(..., description="屋齡")
    average_price: float = Field(..., alias="averagePrice", description="平均價格")
    average_square_feet: float = Field(
        ..., alias="averageSquareFeet", description="平均坪數"
    )
    house_number: str = Field(..., alias="houseNumber", description="門牌號碼")
    building_material: str = Field(..., alias="buildingMaterial", description="建材")
    use_type: str = Field(..., alias="useType", description="使用分區")
    use_partition: str = Field(..., alias="usePartition", description="使用分區類型")
    area: str = Field(..., description="面積")
    nearby_community: List[NearbyCommunity] = Field(
        ..., alias="nearbyCommunity", description="附近社區"
    )
    house_type: int = Field(..., alias="houseType", description="房屋類型")
    administrative_name: str = Field(
        ..., alias="administrativeName", description="行政區名稱"
    )
    totfloor: str = Field(..., description="總樓層")
    located: str = Field(..., description="地段")
    contract_download: List = Field(
        ..., alias="ContractDownload", description="合約下載"
    )
    performance_guarantee: str = Field(
        ..., alias="performanceGuarantee", description="履約保證"
    )
    project_director: Optional[str] = Field(
        None, alias="projectDirector", description="建案主任"
    )
    license: Optional[str] = Field(None, description="執照")
    presold_house_info: bool = Field(
        ..., alias="presoldHouseInfo", description="預售屋資訊"
    )
    good_community: bool = Field(..., alias="goodCommunity", description="優質社區")
    bank: str = Field(..., description="銀行")
    bank_link: str = Field(..., alias="bank_link", description="銀行連結")
    build_type: int = Field(..., alias="buildType", description="建物類型")
    avg_rent_last_year: str = Field(
        ..., alias="avg_rent_last_year", description="去年平均租金"
    )
    avg_rent_all_time: str = Field(
        ..., alias="avg_rent_all_time", description="歷史平均租金"
    )
    highest_rent_all_time: str = Field(
        ..., alias="highest_rent_all_time", description="歷史最高租金"
    )
    lowest_rent_all_time: str = Field(
        ..., alias="lowest_rent_all_time", description="歷史最低租金"
    )
    # 座標資訊
    latitude: float = Field(..., description="緯度")
    longitude: float = Field(..., description="經度")

    class Config:
        populate_by_name = True

    def to_geojson_feature(self) -> HouseFeature:
        """轉換為 GeoJSON Feature 格式"""
        return HouseFeature(
            type="Feature",
            geometry=HouseGeometry(
                type="Point", coordinates=[self.longitude, self.latitude]
            ),
            properties=HouseProperties(
                communityId=self.community_id,
                communityName=self.community_name,
                nowAveragePrice=self.now_average_price,
                nowAveragePriceIsCar=self.now_average_price_is_car,
                historyHeightPrice=self.history_height_price,
                historyHeightPriceIsCar=self.history_height_price_is_car,
                historyAveragePrice=self.history_average_price,
                historyAveragePriceIsCar=self.history_average_price_is_car,
                historyLowPrice=self.history_low_price,
                historyLowPriceIsCar=self.history_low_price_is_car,
                bufferZonesPrice=self.buffer_zones_price,
                bufferZonesPriceIsCar=self.buffer_zones_price_is_car,
                architectureType=self.architecture_type,
                housingTotalNumber=self.housing_total_number,
                age=self.age,
                averagePrice=self.average_price,
                averageSquareFeet=self.average_square_feet,
                houseNumber=self.house_number,
                buildingMaterial=self.building_material,
                useType=self.use_type,
                usePartition=self.use_partition,
                area=self.area,
                nearbyCommunity=self.nearby_community,
                houseType=self.house_type,
                administrativeName=self.administrative_name,
                totfloor=self.totfloor,
                located=self.located,
                ContractDownload=self.contract_download,
                performanceGuarantee=self.performance_guarantee,
                projectDirector=self.project_director,
                license=self.license,
                presoldHouseInfo=self.presold_house_info,
                goodCommunity=self.good_community,
                bank=self.bank,
                bank_link=self.bank_link,
                buildType=self.build_type,
                avg_rent_last_year=self.avg_rent_last_year,
                avg_rent_all_time=self.avg_rent_all_time,
                highest_rent_all_time=self.highest_rent_all_time,
                lowest_rent_all_time=self.lowest_rent_all_time,
            ),
        )


class HouseRawDataList(BaseModel):
    """原始 API 房屋資料列表"""

    data: List[HouseRawData] = Field(..., description="房屋資料列表")

    def to_geojson(self) -> HouseFeatureCollection:
        """轉換為 GeoJSON FeatureCollection 格式"""
        features = [house.to_geojson_feature() for house in self.data]
        return HouseFeatureCollection(type="FeatureCollection", features=features)
