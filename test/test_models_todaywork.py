from app.models.todaywork import WorkFeatureCollection

TESTDATA = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [301516.593, 2769209.131]},
            "properties": {
                "Ac_no": "104003395",
                "sno": "22",
                "AppMode": "0",
                "X": "301516.593",
                "Y": "2769209.131",
                "AppTime": "108/01/18 14:59:06",
                "App_Name": "捷運二工處(南區)",
                "C_Name": "中正",
                "Addr": "南海路南海路牯嶺街口至和平西路(含路口)穿越平房至西藏路惠安街",
                "Cb_Da": "114/10/06",
                "Ce_Da": "115/04/02",
                "Co_Ti": "依交維計畫訂定時間施工",
                "Tc_Na": "大陸工程股份有限公司",
                "Tc_Ma": "紀ＯＯ",
                "Tc_Tl": "0902313143",
                "Tc_Ma3": "梁ＯＯ",
                "Tc_Tl3": "0973258333",
                "NPurp": "市政建設(捷運局-捷運工程)",
                "DType": "",
                "DLen": "3087.6",
                "IsStay": "是",
                "IsBlock": "否",
                "PlanB": "",
                "WItem": "",
                "Positions_type": "MultiLineString",
                "Positions": [
                    [
                        [301442.106, 2769263.539],
                        [301441.458, 2769251.88],
                        [301516.593, 2769209.131],
                        [301502.343, 2769192.291],
                        [301418.788, 2769241.517],
                        [301398.709, 2769234.392],
                        [301389.409, 2769230.349],
                        [301365.189, 2769237.469],
                        [301242.773, 2769236.836],
                        [301187.225, 2769253.493],
                        [301149.393, 2769252.342],
                        [301101.918, 2769239.594],
                        [301095.313, 2769253.54],
                        [301093.201, 2769260.518],
                        [301092.686, 2769264.116],
                        [301092.388, 2769267.5],
                        [301163.885, 2769286.232],
                        [301324.819, 2769275.824],
                        [301373.934, 2769286.533],
                        [301390.936, 2769277.304],
                        [301967.751, 2769435.16],
                        [301978.243, 2769422.459],
                        [301441.458, 2769263.539],
                    ],
                    [
                        [301354.176, 2769259.807],
                        [301362.881, 2769254.816],
                        [301367.07, 2769245.427],
                        [301365.198, 2769237.435],
                        [301241.966, 2769236.363],
                        [301187.647, 2769253.338],
                        [301149.734, 2769252.63],
                        [301054.817, 2769226.602],
                        [301041.803, 2769254.045],
                        [301144.644, 2769281.629],
                        [301161.757, 2769284.599],
                        [301185.383, 2769286.156],
                        [301327.402, 2769275.263],
                        [301354.146, 2769259.867],
                    ],
                    [
                        [301823.775, 2769394.987],
                        [301967.485, 2769436.45],
                        [301978.909, 2769421.957],
                        [301828.842, 2769379.124],
                        [301824.179, 2769395.258],
                        [301824.449, 2769395.528],
                    ],
                ],
            },
        },
    ],
}


def test_work_feature_collection():
    collection = WorkFeatureCollection(**TESTDATA)

    assert collection.type == "FeatureCollection"
    assert len(collection.features) == 1

    feature = collection.features[0]
    assert feature.type == "Feature"
    assert feature.geometry.type == "Point"
    assert feature.geometry.coordinates == [301516.593, 2769209.131]

    properties = feature.properties
    assert properties.ac_no == "104003395"
    assert properties.app_name == "捷運二工處(南區)"
    assert (
        properties.addr
        == "南海路南海路牯嶺街口至和平西路(含路口)穿越平房至西藏路惠安街"
    )
    assert properties.cb_da == "114/10/06"
    assert properties.ce_da == "115/04/02"
    assert properties.positions_type == "MultiLineString"
    assert len(properties.positions) == 3


def test_datetime_iso8601_conversion():
    """測試時間轉換為 ISO 8601 格式"""
    collection = WorkFeatureCollection(**TESTDATA)

    json_data = collection.model_dump()

    feature = json_data["features"][0]
    properties = feature["properties"]

    assert properties["app_time"] == "2019-01-18T14:59:06"

    assert properties["cb_da"] == "2025-10-06"

    assert properties["ce_da"] == "2026-04-02"
