from app.models.work_diagram import WorkProjectResponse

TEST_DATA = {
    "result": {
        "limit": 1000,
        "offset": 0,
        "count": 126,
        "sort": "",
        "results": [
            {
                "_id": 1,
                "_importdate": {
                    "date": "2025-08-04 18:23:30.374419",
                    "timezone_type": 3,
                    "timezone": "Asia\/Taipei",
                },
                "序號": "1",
                "工程名稱": "中正橋改建工程",
                "執行機關": "臺北市政府工務局新建工程處",
                "開工日期": "108.05.06",
                "預定完成日期": "114.11.29",
                "決標金額－千元": "2217900",
                "工程位置－經度": "121.5079785",
                "工程位置－緯度": "25.02265781",
            },
            {
                "_id": 2,
                "_importdate": {
                    "date": "2025-08-04 18:23:30.385858",
                    "timezone_type": 3,
                    "timezone": "Asia\/Taipei",
                },
                "序號": "2",
                "工程名稱": "錦州街公共住宅新建工程",
                "執行機關": "臺北市政府工務局新建工程處",
                "開工日期": "109.02.17",
                "預定完成日期": "114.10.10",
                "決標金額－千元": "2205000",
                "工程位置－經度": "121.5188",
                "工程位置－緯度": "25.06156439",
            },
            {
                "_id": 3,
                "_importdate": {
                    "date": "2025-08-04 18:23:30.387190",
                    "timezone_type": 3,
                    "timezone": "Asia\/Taipei",
                },
                "序號": "3",
                "工程名稱": "成功市場改建工程",
                "執行機關": "臺北市政府工務局新建工程處",
                "開工日期": "108.07.29",
                "預定完成日期": "115.04.30",
                "決標金額－千元": "678458",
                "工程位置－經度": "121.5400389",
                "工程位置－緯度": "25.02878073",
            },
        ],
    }
}


def test_work_project_response_model():
    response = WorkProjectResponse(**TEST_DATA["result"])

    assert len(response.results) == 3

    first_project = response.results[0]
    assert first_project.id == 1
    assert first_project.project_name == "中正橋改建工程"
    assert first_project.executing_agency == "臺北市政府工務局新建工程處"
    assert first_project.start_date == "108.05.06"
    assert first_project.expected_completion_date == "114.11.29"
    assert first_project.contract_amount_thousand == "2217900"
    assert first_project.longitude == "121.5079785"
    assert first_project.latitude == "25.02265781"


def test_datetime_iso8601_conversion():
    """測試時間轉換為 ISO 8601 格式"""
    response = WorkProjectResponse(**TEST_DATA["result"])

    # 將模型序列化為 JSON
    json_data = response.model_dump()

    project1 = json_data["results"][0]
    project2 = json_data["results"][1]
    project3 = json_data["results"][2]

    # 驗證匯入日期轉換：2025-08-04 18:23:30.374419 -> 2025-08-04T18:23:30.374419
    assert project1["import_date"]["date"] == "2025-08-04T18:23:30.374419"
    assert project2["import_date"]["date"] == "2025-08-04T18:23:30.385858"
    assert project3["import_date"]["date"] == "2025-08-04T18:23:30.387190"

    # 驗證開工日期轉換：108.05.06 -> 2019-05-06
    assert project1["start_date"] == "2019-05-06"
    assert project2["start_date"] == "2020-02-17"
    assert project3["start_date"] == "2019-07-29"

    # 驗證預定完成日期轉換：114.11.29 -> 2025-11-29
    assert project1["expected_completion_date"] == "2025-11-29"
    assert project2["expected_completion_date"] == "2025-10-10"
    assert project3["expected_completion_date"] == "2026-04-30"

