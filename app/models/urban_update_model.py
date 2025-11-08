from typing import List, Optional
from pydantic import BaseModel, Field

class UrbanRecord(BaseModel):
    date: Optional[str] = Field(None, description="資料日期")
    title: Optional[str] = Field(None, description="案件名稱")
    area: Optional[float] = Field(None, description="面積")
    update_type: Optional[str] = Field(
        None, alias="updateType", description="更新地區類型"
    )
    announcement_date: Optional[str] = Field(
        None, alias="announcementDate", description="公告日期"
    )
    update_area_size: Optional[str] = Field(
        None, alias="updateAreaSize", description="更新地區面積"
    )
    coordinates: Optional[list] = Field(None, description="地理座標")

    class Config:
        populate_by_name = True
        json_encoders = {
            float: lambda v: round(v, 2) if v is not None else None
        }

class UrbanUpdateResponse(BaseModel):
    status: str = Field(..., description="回傳狀態 (success / empty / error)")
    districts: str = Field(..., description="行政區名稱")
    records: List[UrbanRecord] = Field(default_factory=list, description="更新紀錄")
    record_count: int = Field(default=0, description="記錄數量")

    def __init__(self, **data):
        super().__init__(**data)
        self.record_count = len(self.records)

    class Config:
        populate_by_name = True


class UrbanUpdateListResponse(BaseModel):
    status: str = Field(..., description="回傳狀態 (success / empty / error)")
    data: List[UrbanUpdateResponse] = Field(default_factory=list)
    total_count: int = Field(default=0, description="總數量")

    def __init__(self, **data):
        super().__init__(**data)
        self.total_count = len(self.data)

    class Config:
        populate_by_name = True
