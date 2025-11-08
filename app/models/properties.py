from typing import List, Literal
from pydantic import BaseModel, Field


class Properties(BaseModel):
    stroke_color: str = Field(alias="stroke-color", description="邊框顏色")
    stroke_width: int = Field(alias="stroke-width", description="邊框寬度")
    stroke_opacity: float = Field(alias="stroke-opacity", description="邊框透明度")
    fill_color: str = Field(alias="fill-color", description="填充顏色")
    fill_opacity: float = Field(alias="fill-opacity", description="填充透明度")
    id: str = Field(alias="ID", description="ID")
    case_number: str = Field(alias="案件編號", description="案件編號")

    class Config:
        populate_by_name = True


class Geometry(BaseModel):
    type: Literal[
        "Polygon",
        "Point",
        "LineString",
        "MultiPolygon",
        "MultiPoint",
        "MultiLineString",
    ]
    coordinates: List[List[List[float]]]


class Feature(BaseModel):
    type: Literal["Feature"]
    properties: Properties
    geometry: Geometry


class FeatureCollection(BaseModel):
    type: Literal["FeatureCollection"]
    features: List[Feature]
