from app.models.earthquakes_building import EarthquakeBuildingResponse


TEST_DATA = {
    "result": {
        "limit": 1,
        "offset": 0,
        "count": 40,
        "sort": "",
        "results": [
            {
                "_id": 1,
                "_importdate": {
                    "date": "2025-10-09 17:41:10.275641",
                    "timezone_type": 3,
                    "timezone": "Asia\/Taipei",
                },
                "縣市別": "臺北市",
                "縣市別代碼": "63000",
                "行政區": "士林區",
                "行政區代碼（編碼）": "111",
                "建築地點": "天母北路87巷22弄2、4、6號； 87巷16至22號1至5樓",
                "備註": "921黃單",
            }
        ],
    }
}


def test_earthquake_building_response():
    response = EarthquakeBuildingResponse(**TEST_DATA) # type: ignore

    assert response.result.limit == 1
    assert response.result.offset == 0
    assert response.result.count == 40
    assert response.result.sort == ""
    assert len(response.result.results) == 1

    item = response.result.results[0]
    assert item.id == 1
    assert item.import_date.date == "2025-10-09 17:41:10.275641"
    assert item.import_date.timezone_type == 3
    assert item.county == "臺北市"
    assert item.county_code == "63000"
    assert item.district == "士林區"
    assert item.district_code == "111"
    assert item.building_location == "天母北路87巷22弄2、4、6號； 87巷16至22號1至5樓"
    assert item.note == "921黃單"
