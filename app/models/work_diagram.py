from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, field_serializer


class ImportDate(BaseModel):
    date: str = Field(description="匯入日期時間")
    timezone_type: int = Field(description="時區類型")
    timezone: str = Field(description="時區")

    @field_serializer("date")
    def serialize_date(self, value: str) -> str:
        if not value:
            return value

        try:
            dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
            return dt.isoformat()
        except ValueError:
            try:
                dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                return dt.isoformat()
            except ValueError:
                pass

        return value


class WorkProject(BaseModel):
    id: int = Field(alias="_id", description="ID")
    import_date: ImportDate = Field(alias="_importdate", description="匯入日期")
    serial_number: str = Field(alias="序號", description="序號")
    project_name: str = Field(alias="工程名稱", description="工程名稱")
    executing_agency: str = Field(alias="執行機關", description="執行機關")
    start_date: str = Field(alias="開工日期", description="開工日期")
    expected_completion_date: str = Field(
        alias="預定完成日期", description="預定完成日期"
    )
    contract_amount_thousand: str = Field(
        alias="決標金額－千元", description="決標金額（千元）"
    )
    longitude: str = Field(alias="工程位置－經度", description="工程位置經度")
    latitude: str = Field(alias="工程位置－緯度", description="工程位置緯度")

    @field_serializer("start_date", "expected_completion_date")
    def serialize_roc_date(self, value: str) -> str:
        """將台灣民國日期轉換為 ISO 8601 格式"""
        if not value:
            return value

        try:
            year, month, day = value.split(".")

            year = int(year) + 1911
            dt = datetime.strptime(f"{year}/{month}/{day}", "%Y/%m/%d")
            return dt.date().isoformat()
        except (ValueError, AttributeError):
            pass

        return value

    class Config:
        populate_by_name = True


class WorkProjectResponse(BaseModel):
    results: List[WorkProject] = Field(description="工程專案列表")
