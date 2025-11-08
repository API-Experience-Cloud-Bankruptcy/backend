import json
import re
from datetime import datetime

# === 1️⃣ 讀取分析後的 grouped 檔案 ===
with open("./app/utils/analysis_grouped.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# === 2️⃣ 日期轉換輔助函式 ===
def to_iso_date(date_str):
    """
    將日期轉換成 YYYY-MM-DD 格式。
    支援：
      - 民國年格式: 114.08.29 → 2025-08-29
      - 西元年格式: 2025-08-29 或 2025/08/29
    """
    if not date_str:
        return None

    date_str = date_str.strip()

    # 民國年格式
    m = re.match(r"^(\d{2,3})[./年-](\d{1,2})[./月-](\d{1,2})", date_str)
    if m and int(m.group(1)) < 200:
        year = int(m.group(1)) + 1911
        month = int(m.group(2))
        day = int(m.group(3))
        return f"{year:04d}-{month:02d}-{day:02d}"

    # 西元格式
    try:
        date_obj = datetime.strptime(date_str.replace("/", "-"), "%Y-%m-%d")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        pass

    return date_str  # 無法解析就原樣返回

# === 3️⃣ 轉換所有紀錄的日期 ===
for group in data:
    for rec in group.get("records", []):
        rec["date"] = to_iso_date(rec.get("date"))
        rec["announcementDate"] = to_iso_date(rec.get("announcementDate"))

# === 4️⃣ 輸出為新檔案 ===
with open("./app/utils/analysis_grouped_iso.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ 已輸出成 analysis_grouped_iso.json（日期皆為 YYYY-MM-DD 格式）")
