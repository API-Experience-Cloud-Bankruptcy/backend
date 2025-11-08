from datetime import datetime
from typing import List, Literal, Union
from pydantic import BaseModel, Field, field_serializer


class WorkProperties(BaseModel):
    """道路施工屬性"""

    ac_no: str = Field(alias="Ac_no", description="申請編號")
    sno: str = Field(alias="sno", description="序號")
    app_mode: str = Field(alias="AppMode", description="申請模式")
    x: str = Field(alias="X", description="X 座標")
    y: str = Field(alias="Y", description="Y 座標")
    app_time: str = Field(alias="AppTime", description="申請時間")
    app_name: str = Field(alias="App_Name", description="申請單位名稱")
    c_name: str = Field(alias="C_Name", description="行政區名稱")
    addr: str = Field(alias="Addr", description="施工地址")
    cb_da: str = Field(alias="Cb_Da", description="施工開始日期")
    ce_da: str = Field(alias="Ce_Da", description="施工結束日期")
    co_ti: str = Field(alias="Co_Ti", description="施工時間")

    @field_serializer("app_time", "cb_da", "ce_da")
    def serialize_datetime(self, value: str) -> str:
        """將台灣民國日期時間轉換為 ISO 8601 格式"""
        if not value:
            return value

        try:
            if " " in value:
                date_part, time_part = value.split(" ")
                year, month, day = date_part.split("/")

                year = int(year) + 1911
                dt = datetime.strptime(
                    f"{year}/{month}/{day} {time_part}", "%Y/%m/%d %H:%M:%S"
                )
                return dt.isoformat()

            elif "/" in value:
                year, month, day = value.split("/")

                year = int(year) + 1911
                dt = datetime.strptime(f"{year}/{month}/{day}", "%Y/%m/%d")
                return dt.date().isoformat()
        except (ValueError, AttributeError):
            pass

        return value

    tc_na: str = Field(alias="Tc_Na", description="施工廠商名稱")
    tc_ma: str = Field(alias="Tc_Ma", description="施工廠商負責人")
    tc_tl: str = Field(alias="Tc_Tl", description="施工廠商電話")
    tc_ma3: str = Field(alias="Tc_Ma3", description="施工廠商聯絡人")
    tc_tl3: str = Field(alias="Tc_Tl3", description="施工廠商聯絡人電話")
    n_purp: str = Field(alias="NPurp", description="施工目的")
    d_type: str = Field(alias="DType", description="挖掘類型")
    d_len: str = Field(alias="DLen", description="挖掘長度")
    is_stay: str = Field(alias="IsStay", description="是否長期駐留")
    is_block: str = Field(alias="IsBlock", description="是否阻斷")
    plan_b: str = Field(alias="PlanB", description="替代計畫")
    w_item: str = Field(alias="WItem", description="施工項目")
    positions_type: str = Field(alias="Positions_type", description="位置類型")
    positions: Union[List[List[List[float]]], List[List[List[List[float]]]]] = Field(
        alias="Positions", description="位置座標陣列"
    )

    class Config:
        populate_by_name = True


class WorkGeometry(BaseModel):
    """幾何資料"""

    type: Literal[
        "Point",
        "LineString",
        "Polygon",
        "MultiPoint",
        "MultiLineString",
        "MultiPolygon",
    ]
    coordinates: Union[List[float], List[List[float]], List[List[List[float]]]]


class WorkFeature(BaseModel):
    """道路施工 Feature"""

    type: Literal["Feature"]
    geometry: WorkGeometry
    properties: WorkProperties


class WorkFeatureCollection(BaseModel):
    """道路施工 FeatureCollection"""

    type: Literal["FeatureCollection"]
    features: List[WorkFeature]
