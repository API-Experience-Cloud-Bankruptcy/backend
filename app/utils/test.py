import requests

api_url = "https://twur.cpami.gov.tw/api/tgos/get_update_area"
params = {"city_id": 2}

# 關閉 SSL 憑證驗證
response = requests.get(api_url, params=params)
response.raise_for_status()

response.encoding = response.apparent_encoding
data_utf8 = response.text.encode("utf-8")

print(data_utf8)

# with open("./cpami_update_area_utf8.json", "wb") as f:
#     f.write(data_utf8)

# print("✅ 已下載並轉換為 UTF-8 編碼 → cpami_update_area_utf8.json")
