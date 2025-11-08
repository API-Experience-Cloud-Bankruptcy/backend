import httpx


def get_geocode_from_arcgis(address: str) -> tuple[float, float] | None:
    """Use ArcGIS API to get latitude and longitude from an address."""
    ARC_GIS_API_URL = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"

    params = {
        "SingleLine": address,
        "f": "json",
        "outSR": '{"wkid":4326}',
        "outFields": "Addr_type,Match_addr,StAddr,City",
        "maxLocations": "6"
    }

    try:
        response = httpx.get(ARC_GIS_API_URL, params=params, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        candidates = data.get("candidates", [])
        if not candidates:
            print(f"找不到地址 '{address}' 的地理編碼")
            return None

        location = candidates[0]["location"]
        return location["x"], location["y"]
    except httpx.HTTPStatusError as e:
        print(f"HTTP 錯誤: {e.response.status_code} 地址: '{address}'")
        return None
    except Exception as e:
        print(f"取得地理編碼時發生錯誤 (地址: '{address}'): {e}")
        return None
