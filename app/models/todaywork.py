from datetime import datetime
from typing import List, Literal, Union, Dict, Any
from pydantic import BaseModel, Field, field_serializer
from pyproj import Transformer


COORD_TRANSFORMER = Transformer.from_crs("EPSG:3826", "EPSG:4326", always_xy=True)


def transform_coordinates(coords: Any, geom_type: str) -> Any:
    """TWD97 TM2 To WGS84"""
    if geom_type == "Point":
        lon, lat = COORD_TRANSFORMER.transform(coords[0], coords[1])
        return [lon, lat]

    elif geom_type in ["LineString", "MultiPoint"]:
        return [
            list(COORD_TRANSFORMER.transform(point[0], point[1])) for point in coords
        ]

    elif geom_type in ["Polygon", "MultiLineString"]:
        return [
            [list(COORD_TRANSFORMER.transform(point[0], point[1])) for point in ring]
            for ring in coords
        ]

    elif geom_type == "MultiPolygon":
        return [
            [
                [
                    list(COORD_TRANSFORMER.transform(point[0], point[1]))
                    for point in ring
                ]
                for ring in polygon
            ]
            for polygon in coords
        ]

    return coords


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
    coordinates: Union[
        List[float],
        List[List[float]],
        List[List[List[float]]],
        List[List[List[List[float]]]],
    ]


class WorkFeature(BaseModel):
    """道路施工 Feature"""

    type: Literal["Feature"]
    geometry: WorkGeometry
    properties: WorkProperties

    @classmethod
    def from_wrong_format(cls, wrong_feature: Dict[str, Any]) -> "WorkFeature":
        properties = dict(wrong_feature.get("properties", {}))
        geometry = wrong_feature.get("geometry", {})

        if "Positions" in properties and "Positions_type" in properties:
            positions_type = properties.pop("Positions_type")
            positions = properties.pop("Positions")

            transformed_coords = transform_coordinates(positions, positions_type)

            return cls(
                type="Feature",
                geometry=WorkGeometry(
                    type=positions_type, coordinates=transformed_coords
                ),
                properties=properties,  # type: ignore
            )

        else:
            geom_type = geometry.get("type", "Point")
            coords = geometry.get("coordinates", [])

            transformed_coords = transform_coordinates(coords, geom_type)

            return cls(
                type="Feature",
                geometry=WorkGeometry(type=geom_type, coordinates=transformed_coords),
                properties=properties,  # type: ignore
            )


class WorkFeatureCollection(BaseModel):
    """道路施工 FeatureCollection"""

    type: Literal["FeatureCollection"]
    features: List[WorkFeature]

    @classmethod
    def from_wrong_format(
        cls, wrong_geojson: Union[Dict[str, Any], "WorkFeatureCollection"]
    ) -> "WorkFeatureCollection":
        """從錯誤格式轉換為正確格式

        Args:
            wrong_geojson: 必須是原始 dict（不要先 model_validate）

        Returns:
            正確格式的 WorkFeatureCollection（使用 WGS84 座標）
        """
        if isinstance(wrong_geojson, cls):
            return wrong_geojson

        if isinstance(wrong_geojson, dict):
            features = [
                WorkFeature.from_wrong_format(f)
                for f in wrong_geojson.get("features", [])
            ]
            return cls(type="FeatureCollection", features=features)

        raise TypeError(
            f"Expected dict or WorkFeatureCollection, got {type(wrong_geojson)}"
        )
