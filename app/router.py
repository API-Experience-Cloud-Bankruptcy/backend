from fastapi import APIRouter
from app.handlers.urban_update_handler import UrbanUpdateHandler


api_router = APIRouter()

urban_update_handler = UrbanUpdateHandler()

__all__ = ["api_router"]

@api_router.get("/urban-update")
async def urban_update():
    return urban_update_handler.get_urban_updates()

@api_router.get("/urban-update/{district}")
async def urban_update_by_district(district: str):
    return urban_update_handler.get_urban_update_by_district(district)