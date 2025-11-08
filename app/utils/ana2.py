import json

# === 1️⃣ 讀取原始資料 (假設檔名為 data.json) ===
with open("./app/utils/taipei-dugeng-match.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# === 2️⃣ 篩選所需欄位並統一成小寫 ===
selected_fields = ["districts", "DATE", "content", "title", "AREA", "coordinates"]

filtered_data = []
for item in data:
    new_item = {}
    for key in selected_fields:
        lower_key = key.lower()  # 統一小寫
        if key in item:
            new_item[lower_key] = item[key]
        elif key.upper() in item:
            new_item[lower_key] = item[key.upper()]
        else:
            new_item[lower_key] = None  # 若缺值，補 None
    filtered_data.append(new_item)

# === 3️⃣ 輸出為 JSON 檔案 ===
with open("./app/utils/analysis.json", "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)

print("✅ 已輸出成 analysis.json")
