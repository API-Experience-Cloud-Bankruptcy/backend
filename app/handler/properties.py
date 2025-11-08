from typing import Optional
from app.models.properties import FeatureCollection
from app.services.properties import fetch_properties


class PropertiesHandler:
    async def fetch_features(self) -> FeatureCollection:
        features = await fetch_properties()
        return FeatureCollection(type="FeatureCollection", features=features)

    async def fetch_feature_by_id(self, feature_id: str) -> Optional[FeatureCollection]:
        all_features = await self.fetch_features()

        filtered_features = [
            feature
            for feature in all_features.features
            if feature.properties.id == feature_id
        ]

        if not filtered_features:
            return None

        return FeatureCollection(type="FeatureCollection", features=filtered_features)

    async def fetch_features_by_case_number(
        self, case_number: str
    ) -> FeatureCollection:
        all_features = await self.fetch_features()

        filtered_features = [
            feature
            for feature in all_features.features
            if case_number in feature.properties.case_number
        ]

        return FeatureCollection(type="FeatureCollection", features=filtered_features)
