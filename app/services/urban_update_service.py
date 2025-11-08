import json
import os

from app.models.urban_update_model import UrbanUpdateListResponse, UrbanUpdateResponse

class UrbanUpdateService:
    def __init__(self):
        self.file_path = "public/urban-update.json"

    def load_data(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_urbab_updates(self) -> UrbanUpdateListResponse:
        data = self.load_data()
        responses = [
            UrbanUpdateResponse(
                status="success",
                districts=item.get("districts", "未知區"),
                records=item.get("records", []),
            )
            for item in data
        ]
        return UrbanUpdateListResponse(
            status="success" if data else "empty",
            data=responses,
        )

    def get_urban_update_by_district(self, district: str) -> UrbanUpdateResponse:
        data = self.load_data()

        for record in data:
            if record.get("districts") == district:
                return UrbanUpdateResponse(
                    status="success",
                    districts=record.get("districts", district),
                    records=record.get("records", []),
                )

        return UrbanUpdateResponse(
            status="empty",
            districts=district,
            records=[],
        )

if __name__ == "__main__":
    service = UrbanUpdateService()
    updates = service.get_urban_update_by_district("大安區")
    count = len(updates.get("records", []))
    print(f"Found {count} updates for 大安區")
