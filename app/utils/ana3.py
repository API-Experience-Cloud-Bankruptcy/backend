import json
import re

# === 1️⃣ 讀取前一步產生的 analysis.json ===
with open("./app/utils/analysis.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# === 2️⃣ 定義 regex 擷取三種內容 ===
pattern_type = r"更新地區類型:\s*<span>(.*?)</span>"
pattern_date = r"更新地區公告日期:\s*<span>(.*?)</span>"
pattern_area = r"更新地區面積:\s*<span>(.*?)</span>"

# === 3️⃣ 逐筆轉換 content 為扁平化英文鍵 ===
for item in data:
    content = item.get("content", "")
    update_type = re.search(pattern_type, content)
    announcement_date = re.search(pattern_date, content)
    update_area_size = re.search(pattern_area, content)

    # 新增英文鍵
    item["update_type"] = update_type.group(1) if update_type else None
    item["announcement_date"] = announcement_date.group(1) if announcement_date else None
    item["update_area_size"] = update_area_size.group(1) if update_area_size else None

    # 移除原 content 欄位
    item.pop("content", None)

# === 4️⃣ 輸出成新的 JSON ===
with open("./app/utils/analysis_flat.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ 已輸出成 analysis_flat.json（content 已扁平化）")
