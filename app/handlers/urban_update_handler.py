from fastapi import HTTPException
from app.services.urban_update_service import UrbanUpdateService
from app.models.urban_update_model import UrbanUpdateListResponse, UrbanUpdateResponse

class UrbanUpdateHandler:
    def __init__(self):
        self.service = UrbanUpdateService()

    def get_urban_updates(self) -> UrbanUpdateListResponse:
        data = self.service.get_urbab_updates()
        if data.status == "empty":
            raise HTTPException(status_code=404, detail="Urban update data not found")
        return data

    def get_urban_update_by_district(self, district: str) -> UrbanUpdateResponse:
        data = self.service.get_urban_update_by_district(district)
        if data.status == "empty":
            raise HTTPException(
                status_code=404,
                detail=f"No urban update data found for district: {district}",
            )
        return data


# ✅ for quick testing
if __name__ == "__main__":
    handler = UrbanUpdateHandler()
    updates = handler.get_urban_update_by_district("大安區")
    count = len(updates.records)
    print(f"Found {count} updates for {updates.districts}")
