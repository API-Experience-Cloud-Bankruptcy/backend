import json
from pathlib import Path
from typing import List
from app.models.chloride_ionized_concrete_geojson import (
    ChlorideIonizedConcreteFeatureCollection,
    ChlorideIonizedConcreteFeature,
    ChlorideIonizedConcreteGeometry,
    ChlorideIonizedConcreteProperties,
    ImportDate,
)


JSON_FILE_PATH = (
    Path(__file__).parent.parent.parent
    / "data"
    / "chloride_ionized_concrete_format.json"
)


async def load_chloride_ionized_concrete_geojson() -> (
    ChlorideIonizedConcreteFeatureCollection
):
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    features: List[ChlorideIonizedConcreteFeature] = []

    for item in data["result"]:
        properties = ChlorideIonizedConcreteProperties(
            id=item["id"],
            import_date=ImportDate(**item["import_date"]),
            county=item["county"],
            county_code=item["county_code"],
            item_number=item["item_number"],
            organizer=item["organizer"],
            district=item["district"],
            district_code=item["district_code"],
            building_name=item["building_name"],
            purpose=item["purpose"],
            building_location=item["building_location"],
        )

        geometry = ChlorideIonizedConcreteGeometry(
            coordinates=[item["longitude"], item["latitude"]]
        )

        feature = ChlorideIonizedConcreteFeature(
            properties=properties, geometry=geometry
        )

        features.append(feature)

    return ChlorideIonizedConcreteFeatureCollection(features=features)
