from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.handler.todaywork import TodayWorkHandler
from app.handler.work_diagram import WorkDiagramHandler
from app.handler.properties import PropertiesHandler
from app.models.todaywork import WorkFeatureCollection
from app.models.work_diagram import WorkProject
from app.models.properties import FeatureCollection

api_router = APIRouter()

todaywork_handler = TodayWorkHandler()
work_diagram_handler = WorkDiagramHandler()
properties_handler = PropertiesHandler()


@api_router.get(
    "/todaywork",
    response_model=WorkFeatureCollection,
    tags=["今日施工"],
    response_model_by_alias=False,
)
async def get_today_work():
    return await todaywork_handler.fetch_work_data()


@api_router.get(
    "/todaywork/district/{district}",
    response_model=WorkFeatureCollection,
    tags=["今日施工"],
    response_model_by_alias=False,
)
async def get_work_by_district(district: str):
    result = await todaywork_handler.fetch_work_by_district(district)
    if not result.features:
        raise HTTPException(status_code=404, detail=f"查無 {district} 區的施工資料")
    return result


@api_router.get(
    "/todaywork/contractor",
    response_model=WorkFeatureCollection,
    tags=["今日施工"],
    response_model_by_alias=False,
)
async def get_work_by_contractor(contractor: str = Query(...)):
    result = await todaywork_handler.fetch_work_by_contractor(contractor)
    if not result.features:
        raise HTTPException(
            status_code=404, detail=f"查無廠商「{contractor}」的施工資料"
        )
    return result


@api_router.get(
    "/projects",
    response_model=List[WorkProject],
    tags=["工程專案"],
    response_model_by_alias=False,
)
async def get_projects():
    return await work_diagram_handler.fetch_projects()


@api_router.get(
    "/projects/{project_id}",
    response_model=WorkProject,
    tags=["工程專案"],
    response_model_by_alias=False,
)
async def get_project_by_id(project_id: int):
    project = await work_diagram_handler.fetch_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=404, detail=f"查無 ID 為 {project_id} 的工程專案"
        )
    return project


@api_router.get(
    "/projects/search/by-agency",
    response_model=List[WorkProject],
    tags=["工程專案"],
    response_model_by_alias=False,
)
async def search_projects_by_agency(agency: str = Query(...)):
    projects = await work_diagram_handler.fetch_projects_by_agency(agency)
    if not projects:
        raise HTTPException(
            status_code=404, detail=f"查無執行機關「{agency}」的工程專案"
        )
    return projects


@api_router.get(
    "/projects/search/by-name",
    response_model=List[WorkProject],
    tags=["工程專案"],
    response_model_by_alias=False,
)
async def search_projects_by_name(keyword: str = Query(...)):
    projects = await work_diagram_handler.fetch_projects_by_name(keyword)
    if not projects:
        raise HTTPException(status_code=404, detail=f"查無包含「{keyword}」的工程專案")
    return projects


@api_router.get(
    "/properties",
    response_model=FeatureCollection,
    tags=["都市更新"],
)
async def get_properties():
    return await properties_handler.fetch_features()


@api_router.get(
    "/properties/{feature_id}",
    response_model=FeatureCollection,
    tags=["都市更新"],
)
async def get_property_by_id(feature_id: str):
    result = await properties_handler.fetch_feature_by_id(feature_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"查無 ID 為 {feature_id} 的特徵")
    return result


@api_router.get(
    "/properties/case/{case_number}",
    response_model=FeatureCollection,
    tags=["都市更新"],
)
async def get_properties_by_case(case_number: str):
    result = await properties_handler.fetch_features_by_case_number(case_number)
    if not result.features:
        raise HTTPException(
            status_code=404, detail=f"查無案件編號「{case_number}」的特徵"
        )
    return result


@api_router.get("/health", tags=["系統"])
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
    }


__all__ = ["api_router"]
