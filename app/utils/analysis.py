import pandas as pd
import json

taipei_districts = [
    "中正區", "大同區", "中山區", "松山區", "大安區",
    "信義區", "內湖區", "南港區", "士林區", "北投區",
    "文山區", "萬華區"
]

# === 讀取與展開 GeoJSON ===
data = pd.read_json("./app/utils/taipei-dugeng.json")
df = pd.json_normalize(data["features"])

# 只取 properties 和 geometry.coordinates
df = df[[col for col in df.columns if col.startswith("properties.") or col == "geometry.coordinates"]]

# 改欄名：去掉 properties. 前綴，改成 coordinates
df.columns = [col.replace("properties.", "") if col != "geometry.coordinates" else "coordinates" for col in df.columns]

# === 預先建立 districts 欄位 ===
df["districts"] = None

# === 遍歷並更新 districts ===
no_match_count = 0
for i, row in df.iterrows():
    found = [d for d in taipei_districts if any(d in str(v) for v in row.values)]
    if found:
        df.at[i, "districts"] = ",".join(found)
    else:
        no_match_count += 1

print(f"✅ 有找到行政區的筆數: {len(df) - no_match_count}")
print(f"❌ 沒有找到行政區的筆數: {no_match_count}")

# === 分組 ===
df_match = df[df["districts"].notna()]
df_no_match = df[df["districts"].isna()]

# === 將 DataFrame 轉為乾淨 JSON（去掉 None/NaN/空字串） ===
def df_to_clean_json(df, path):
    records = df.to_dict(orient="records")
    cleaned = []
    for rec in records:
        new_rec = {}
        for k, v in rec.items():
            # 保留 coordinates，即使為空也保留
            if k == "coordinates":
                new_rec[k] = v
                continue
            # 移除 None / NaN / 空字串 / 空容器
            if pd.isna(v) or v in ["", [], {}, None]:
                continue
            new_rec[k] = v
        cleaned.append(new_rec)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    print(f"💾 已輸出乾淨 JSON → {path}")

# === 輸出兩份 JSON ===
path_match = "./app/utils/taipei-dugeng-match.json"
path_no_match = "./app/utils/taipei-dugeng-no-match.json"
df_to_clean_json(df_match, path_match)
df_to_clean_json(df_no_match, path_no_match)
