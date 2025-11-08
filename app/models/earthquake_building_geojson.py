from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class ImportDate(BaseModel):
    """匯入日期資訊"""

    date: str = Field(description="匯入日期時間")
    timezone_type: int = Field(description="時區類型")
    timezone: str = Field(description="時區")


class EarthquakeBuildingProperties(BaseModel):
    """地震建築物屬性"""

    id: int = Field(description="項目 ID")
    import_date: ImportDate = Field(description="匯入日期")
    county: str = Field(description="縣市別")
    county_code: str = Field(description="縣市別代碼")
    district: str = Field(description="行政區")
    district_code: str = Field(description="行政區代碼")
    building_location: str = Field(description="建築地點")
    note: Optional[str] = Field(default=None, description="備註")


class EarthquakeBuildingGeometry(BaseModel):
    """GeoJSON 幾何資訊"""

    type: Literal["MultiPoint"] = "MultiPoint"
    coordinates: List[List[float]] = Field(description="座標列表 [[經度, 緯度], ...]")


class EarthquakeBuildingFeature(BaseModel):
    """地震建築物 GeoJSON Feature"""

    type: Literal["Feature"] = "Feature"
    properties: EarthquakeBuildingProperties
    geometry: EarthquakeBuildingGeometry


class EarthquakeBuildingFeatureCollection(BaseModel):
    """地震建築物 GeoJSON FeatureCollection"""

    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: List[EarthquakeBuildingFeature]
