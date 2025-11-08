import json
from collections import defaultdict

# === 1️⃣ 讀取前一步輸出的 analysis_flat.json ===
with open("./app/utils/analysis_flat.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# === 2️⃣ 按 districts 聚合 ===
grouped = defaultdict(list)

for item in data:
    district = item.get("districts", "未知地區")
    record = {
        "date": item.get("date"),
        "title": item.get("title"),
        "area": item.get("area"),
        "updateType": item.get("update_type"),
        "announcementDate": item.get("announcement_date"),
        "updateAreaSize": item.get("update_area_size"),
        "coordinates": item.get("coordinates")
    }
    grouped[district].append(record)

# === 3️⃣ 轉換為指定格式 ===
output = []
for district, records in grouped.items():
    output.append({
        "districts": district,
        "records": records
    })

# === 4️⃣ 寫出成 JSON ===
with open("./app/utils/analysis_grouped.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("✅ 已輸出成 analysis_grouped.json（依照 districts 聚合完成）")
