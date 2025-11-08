import json
from datetime import datetime

# === 1️⃣ 讀取前一版 grouped_iso.json ===
with open("./app/utils/analysis_grouped_iso.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# === 2️⃣ 建立 meta 區塊 ===
meta = {
    "city": "臺北市",
    "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# === 3️⃣ 將欄位轉為 API-friendly 格式 ===
api_data = []
for group in data:
    district_name = group.get("districts", "未知地區")
    records = []

    for r in group.get("records", []):
        # 將字串數字轉成 float（若失敗就保留原值）
        def parse_float(val):
            try:
                return float(str(val).replace(",", ""))
            except:
                return val

        record = {
            "date": r.get("date"),
            "title": r.get("title"),
            "area": parse_float(r.get("area")),
            "updateType": r.get("update_type"),
            "announcementDate": r.get("announcement_date"),
            "updateAreaSize": parse_float(r.get("update_area_size")),
            "coordinates": r.get("coordinates")
        }
        records.append(record)

    api_data.append({
        "district": district_name,
        "records": records
    })

# === 4️⃣ 包成最終 API 結構 ===
output = {
    "meta": meta,
    "data": api_data
}

# === 5️⃣ 輸出成 JSON ===
with open("./app/utils/analysis_api_ready.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("✅ 已輸出成 analysis_api_ready.json（適合 API 回傳格式）")
