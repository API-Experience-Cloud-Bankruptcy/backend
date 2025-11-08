import httpx
import os
import pandas as pd

API_KEY = os.getenv("WEATHER_API_KEY")
API_URL = "https://data.moenv.gov.tw/api/v2/aqx_p_136"


def fetch_taipei_air_quality():
    params = {"api_key": API_KEY, "limit": 4000, "language": "zh"}
    response = httpx.get(API_URL, params=params)
    if response.status_code != 200:
        return

    try:
        data = response.json().get("records", [])
        df = pd.DataFrame(data)
        if df.empty:
            return
        df["concentration"] = pd.to_numeric(df["concentration"], errors="coerce")
        df = df[["sitename", "monitordate", "itemengname", "concentration"]]
        df.to_csv("data/taipei_air_quality.csv", index=False)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    API_KEY = os.getenv("WEATHER_API_KEY")
    print(os.getenv("WEATHER_API_KEY"))
    fetch_taipei_air_quality()
