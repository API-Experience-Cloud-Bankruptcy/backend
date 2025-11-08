from typing import List, Literal
from pydantic import BaseModel, Field


class ImportDate(BaseModel):
    """匯入日期資訊"""

    date: str = Field(description="匯入日期時間")
    timezone_type: int = Field(description="時區類型")
    timezone: str = Field(description="時區")


class ChlorideIonizedConcreteProperties(BaseModel):
    """海砂屋建築物屬性"""

    id: int = Field(description="項目 ID")
    import_date: ImportDate = Field(description="匯入日期")
    county: str = Field(description="縣市別")
    county_code: str = Field(description="縣市別代碼")
    item_number: str = Field(description="項次")
    organizer: str = Field(description="主辦(管)單位")
    district: str = Field(description="行政區")
    district_code: str = Field(description="行政區代碼")
    building_name: str = Field(description="建築物名稱")
    purpose: str = Field(description="使用目的")
    building_location: str = Field(description="建築地點")


class ChlorideIonizedConcreteGeometry(BaseModel):
    """GeoJSON 幾何資訊"""

    type: Literal["Point"] = "Point"
    coordinates: List[float] = Field(description="座標 [經度, 緯度]")


class ChlorideIonizedConcreteFeature(BaseModel):
    """海砂屋建築物 GeoJSON Feature"""

    type: Literal["Feature"] = "Feature"
    properties: ChlorideIonizedConcreteProperties
    geometry: ChlorideIonizedConcreteGeometry


class ChlorideIonizedConcreteFeatureCollection(BaseModel):
    """海砂屋建築物 GeoJSON FeatureCollection"""

    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: List[ChlorideIonizedConcreteFeature]
