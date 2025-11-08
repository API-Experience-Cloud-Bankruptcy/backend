from app.models.chloride_Ionized_concrete import ChlorideIonizedConcreteResponse

TEST_DATA = {
    "result": {
        "limit": 1,
        "offset": 0,
        "count": 12,
        "sort": "",
        "results": [
            {
                "_id": 1,
                "_importdate": {
                    "date": "2025-10-09 17:41:12.614221",
                    "timezone_type": 3,
                    "timezone": "Asia\/Taipei",
                },
                "縣市別": "臺北市",
                "縣市別代碼": "63000",
                "項次": "1",
                "主辦（管）單位": "臺北市政府衛生局(臺北市立聯合醫院)",
                "行政區": "南港區",
                "行政區代碼（編碼）": "115",
                "建築物名稱": "忠孝院區醫療大樓行政大樓",
                "使用目的": "醫院",
                "建築地點": "南港區同德路87號",
            }
        ],
    }
}


def test_chloride_ionized_concrete_response():
    response = ChlorideIonizedConcreteResponse(**TEST_DATA)  # type: ignore

    assert response.result.limit == 1
    assert response.result.offset == 0
    assert response.result.count == 12
    assert response.result.sort == ""
    assert len(response.result.results) == 1

    item = response.result.results[0]
    assert item.id == 1
    assert item.import_date.date == "2025-10-09 17:41:12.614221"
    assert item.import_date.timezone_type == 3
    assert item.county == "臺北市"
    assert item.county_code == "63000"
    assert item.item_number == "1"
    assert item.organizer == "臺北市政府衛生局(臺北市立聯合醫院)"
    assert item.district == "南港區"
    assert item.district_code == "115"
    assert item.building_name == "忠孝院區醫療大樓行政大樓"
    assert item.purpose == "醫院"
    assert item.building_location == "南港區同德路87號"
