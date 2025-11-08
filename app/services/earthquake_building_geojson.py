import json
from pathlib import Path
from typing import List
from app.models.earthquake_building_geojson import (
    EarthquakeBuildingFeatureCollection,
    EarthquakeBuildingFeature,
    EarthquakeBuildingGeometry,
    EarthquakeBuildingProperties,
    ImportDate,
)


JSON_FILE_PATH = (
    Path(__file__).parent.parent.parent
    / "data"
    / "fetch_earthquake_buildings_format.json"
)


async def load_earthquake_buildings_geojson() -> EarthquakeBuildingFeatureCollection:
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    features: List[EarthquakeBuildingFeature] = []

    for item in data["result"]:
        properties = EarthquakeBuildingProperties(
            id=item["id"],
            import_date=ImportDate(**item["import_date"]),
            county=item["county"],
            county_code=item["county_code"],
            district=item["district"],
            district_code=item["district_code"],
            building_location=item["building_location"],
            note=item.get("note"),
        )

        coordinates = [
            [geo["longitude"], geo["latitude"]] for geo in item.get("geo", [])
        ]
        geometry = EarthquakeBuildingGeometry(coordinates=coordinates)

        feature = EarthquakeBuildingFeature(properties=properties, geometry=geometry)

        features.append(feature)

    return EarthquakeBuildingFeatureCollection(features=features)
