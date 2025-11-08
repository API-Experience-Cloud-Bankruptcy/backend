import asyncio
import json
import sys
from pathlib import Path
import httpx
import re
from typing import List, Set

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from app.models.earthquakes_building import (
    EarthquakeBuildingFormatResponse,
    EarthquakeBuildingItemFormat,
    EarthquakeBuildingItemGeoList,
    EarthquakeBuildingResponse,
)


from data.util import get_geocode_from_arcgis

API_URL = "https://data.taipei/api/v1/dataset/a6e8f08e-ec2a-4be7-a762-54452b0c27df"


def extract_addresses(text: str) -> List[str]:
    """提取並展開台灣地址"""
    addresses = set()

    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"\d+至\d+樓", "", text)

    segments = re.split(r"[;；]", text)

    last_road = ""

    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue

        road_match = re.search(r"(.*?路(?:.*?段)?)", segment)
        if road_match:
            last_road = road_match.group(1)

        process_segment(segment, last_road, addresses)

    return sorted(list(addresses))


def process_segment(segment: str, last_road: str, addresses: Set[str]):
    """處理單個段落"""

    if "至" in segment:
        handle_range(segment, last_road, addresses)
        return

    if "、" in segment:
        handle_enumeration(segment, addresses)
        return

    handle_single(segment, addresses)


def handle_enumeration(segment: str, addresses: Set[str]):
    """處理頓號分隔的號碼：2、4、6號"""

    base_match = re.match(r"(.*?路(?:.*?段)?\d+巷(?:\d+弄)?)", segment)

    if not base_match:
        base_match = re.match(r"(.*?路(?:.*?段)?)", segment)

    if not base_match:
        return

    base_addr = base_match.group(1)
    remaining = segment[len(base_addr) :]

    numbers = re.findall(r"(\d+)(?=號|、)", remaining)

    for num in numbers:
        addresses.add(f"{base_addr}{num}號")


def handle_range(segment: str, last_road: str, addresses: Set[str]):
    """處理範圍表示：16至22號 或 17至33之1號"""

    base_addr = ""

    full_match = re.match(r"(.*?路(?:.*?段)?\d+巷(?:\d+弄)?)", segment)
    if full_match:
        base_addr = full_match.group(1)
    else:
        road_match = re.match(r"(.*?路(?:.*?段)?)", segment)
        if road_match:
            base_addr = road_match.group(1)
        else:
            lane_match = re.match(r"(\d+巷)(?:\d+弄)?", segment)
            if lane_match and last_road:
                base_addr = last_road + lane_match.group(1)

    if not base_addr:
        return

    range_match = re.search(r"(\d+)至(\d+)(之\d+)?號", segment)
    if not range_match:
        return

    start = int(range_match.group(1))
    end = int(range_match.group(2))
    suffix = range_match.group(3) or ""

    for num in range(start, end + 1):
        addresses.add(f"{base_addr}{num}{suffix}號")


def handle_single(segment: str, addresses: Set[str]):
    """處理單一地址"""

    match = re.search(r"(.*?路(?:.*?段)?(?:\d+巷)?(?:\d+弄)?\d+(?:之\d+)?號)", segment)
    if match:
        addresses.add(match.group(1))


async def fetch_fetch_earthquake_buildings() -> None:
    async with httpx.AsyncClient() as client:
        params = {"limit": 2000, "offset": 0, "scope": "resourceAquire"}
        response = await client.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        fetch_earthquake_buildings_response = EarthquakeBuildingResponse.model_validate(
            data
        )

        fetch_earthquake_buildings_responses = []
        for item in fetch_earthquake_buildings_response.result.results:
            codes = extract_addresses(item.building_location)
            geolist = []
            for code in codes:
                longitude, latitude = get_geocode_from_arcgis(item.county + code) or (
                    0.0,
                    0.0,
                )
                geolist.append(
                    EarthquakeBuildingItemGeoList(
                        longitude=longitude,
                        latitude=latitude,
                    )
                )
                await asyncio.sleep(0.1)
                print(f"Processed: {code}")

            item_with_coords = EarthquakeBuildingItemFormat(
                **item.model_dump(),
                geo=geolist,
            )
            fetch_earthquake_buildings_responses.append(item_with_coords)
        format_response = EarthquakeBuildingFormatResponse(
            result=fetch_earthquake_buildings_responses
        )

        with open(
            "data/fetch_earthquake_buildings_format.json", "w", encoding="utf-8"
        ) as f:
            json.dump(
                format_response.model_dump(),
                f,
                ensure_ascii=False,
                indent=4,
            )


# def main():
#     test_cases = [
#         "天母北路87巷22弄2、4、6號； 87巷16至22號1至5樓",
#         "延平北路五段213巷17至33之1號",
#         "知行路62至74號(其中知行路64、66號地下一樓及地上一.二.三.四.五樓建築物撤銷列管)、(同知行路60巷1號)",
#         "清江路156號1樓",
#         "中央北路四段442巷4弄2至10號",
#     ]

#     for i, test in enumerate(test_cases, 1):
#         print(f"\n{'=' * 70}")
#         print(f"測試案例 {i}:")
#         print(f"輸入: {test}")
#         print("\n輸出:")

#         results = extract_addresses(test)
#         for addr in results:
#             print(f"  {addr}")


if __name__ == "__main__":
    asyncio.run(fetch_fetch_earthquake_buildings())
