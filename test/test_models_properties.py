from app.models.properties import Feature

TESTDATA = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "stroke-color": "#FF0000",
                "stroke-width": 3,
                "stroke-opacity": 1,
                "fill-color": "#FF0000",
                "fill-opacity": 0.5,
                "ID": "1281",
                "案件編號": "R090502",
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [121.576233283248, 25.0499061744504],
                        [121.576053854637, 25.0499023834549],
                        [121.576078172862, 25.0496262120661],
                        [121.576208543236, 25.0496319808934],
                        [121.576255651833, 25.0496370344067],
                        [121.576233283248, 25.0499061744504],
                    ]
                ],
            },
        }
    ],
}


def test_feature_model():
    feature_data = TESTDATA["features"][0]
    feature = Feature(**feature_data)

    assert feature.type == "Feature"
    assert feature.properties.stroke_color == "#FF0000"
    assert feature.properties.stroke_width == 3
    assert feature.geometry.type == "Polygon"
    assert len(feature.geometry.coordinates) == 1
