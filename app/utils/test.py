#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taiwan Post (中華郵政) 掛號郵件查詢 Demo
自動使用預設 MAIL_ID，輸出成 JSON 檔。
"""

import requests
import json
from datetime import datetime
from pathlib import Path

# 🟢 在這裡直接設定你的掛號號碼（MAIL_ID）
MAIL_ID = "CC123456789TW"  # ← 改成你自己的郵件編號

def query_post_tracking(mail_no: str):
    """查詢郵件追蹤資訊"""
    url = "https://postserv.post.gov.tw/pstmail/EsoafDispatcher"

    payload = {
        "header": {
            "InputVOClass": "com.systex.jbranch.app.server.post.vo.EB500100InputVO",
            "TxnCode": "EB500100",
            "BizCode": "query2",
            "StampTime": True,
            "SupvPwd": "",
            "TXN_DATA": {},
            "SupvID": "",
            "CustID": "",
            "REQUEST_ID": "",
            "ClientTransaction": True,
            "DevMode": False,
            "SectionID": "esoaf"
        },
        "body": {"MAILNO": mail_no, "pageCount": 10}
    }

    # 傳送 POST 請求
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()

    data = resp.json()

    try:
        items = data[0]["body"]["host_rs"]["ITEM"]
    except (KeyError, IndexError, TypeError):
        print("⚠️ 無法解析回應，可能郵件編號錯誤或伺服器異常。")
        return []

    result = []
    for it in items:
        dt_str = it["DATIME"]
        try:
            dt_fmt = datetime.strptime(dt_str, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            dt_fmt = dt_str
        result.append({
            "datetime": dt_fmt,
            "status": it["STATUS"].strip(),
            "station": it["BRHNC"].strip(),
        })

    return result


if __name__ == "__main__":
    results = query_post_tracking(MAIL_ID)

    if not results:
        print("❌ 查詢失敗，請檢查 MAIL_ID 是否正確。")
        exit(1)

    # 儲存為 JSON 檔案
    output_file = Path(f"{MAIL_ID}_tracking.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"✅ 已完成查詢：{MAIL_ID}")
    print(f"📁 結果已儲存：{output_file.resolve()}")
