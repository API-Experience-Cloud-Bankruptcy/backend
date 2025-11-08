from typing import List, Optional
from pydantic import BaseModel, Field


class ImportDate(BaseModel):
    """匯入日期資訊"""

    date: str = Field(description="匯入日期時間")
    timezone_type: int = Field(description="時區類型")
    timezone: str = Field(description="時區")


class EarthquakeBuildingItem(BaseModel):
    """地震建築物資料項目"""

    id: int = Field(alias="_id", description="項目 ID")
    import_date: ImportDate = Field(alias="_importdate", description="匯入日期")
    county: str = Field(alias="縣市別", description="縣市別")
    county_code: str = Field(alias="縣市別代碼", description="縣市別代碼")
    district: str = Field(alias="行政區", description="行政區")
    district_code: str = Field(alias="行政區代碼（編碼）", description="行政區代碼")
    building_location: str = Field(alias="建築地點", description="建築地點")
    note: Optional[str] = Field(default=None, alias="備註", description="備註")

    class Config:
        populate_by_name = True


class EarthquakeBuildingResult(BaseModel):
    """地震建築物查詢結果"""

    limit: int = Field(description="查詢限制數量")
    offset: int = Field(description="查詢偏移量")
    count: int = Field(description="總筆數")
    sort: str = Field(description="排序方式")
    results: List[EarthquakeBuildingItem] = Field(description="查詢結果列表")


class EarthquakeBuildingResponse(BaseModel):
    """地震建築物 API 回應"""

    result: EarthquakeBuildingResult = Field(description="查詢結果")
