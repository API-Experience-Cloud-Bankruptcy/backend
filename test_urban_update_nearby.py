"""
測試都市更新附近搜索功能
"""
from app.services.urban_update_service import UrbanUpdateService

def test_nearby_search():
    """測試附近搜索功能"""
    service = UrbanUpdateService()
    
    # 測試座標：台北市政府
    latitude = 25.0330
    longitude = 121.5654
    search_radius_km = 2.0
    
    print(f"\n🔍 搜索座標: ({latitude}, {longitude})")
    print(f"📏 搜索半徑: {search_radius_km} 公里\n")
    
    try:
        # 測試 search_nearby_updates (包含距離資訊)
        results = service.search_nearby_updates(
            latitude=latitude,
            longitude=longitude,
            search_radius_km=search_radius_km
        )
        
        print(f"✅ 找到 {len(results)} 筆都市更新案件\n")
        
        # 顯示前 5 筆結果
        for i, (record, district, distance) in enumerate(results[:5], 1):
            print(f"[{i}] 距離: {distance:.2f} km")
            print(f"    行政區: {district}")
            print(f"    案件名稱: {record.title}")
            print(f"    面積: {record.area}")
            print(f"    更新類型: {record.update_type}")
            print(f"    公告日期: {record.announcement_date}")
            print()
        
        # 測試 get_nearby_updates (按行政區分組)
        response = service.get_nearby_updates(
            latitude=latitude,
            longitude=longitude,
            search_radius_km=search_radius_km
        )
        
        print(f"📦 按行政區分組:")
        print(f"   狀態: {response.status}")
        print(f"   總行政區數: {response.total_count}")
        
        for district_data in response.data:
            print(f"\n   {district_data.districts}: {district_data.record_count} 筆")
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()


def test_different_locations():
    """測試不同地點"""
    service = UrbanUpdateService()
    
    locations = [
        ("台北市政府", 25.0330, 121.5654),
        ("台北車站", 25.0478, 121.5170),
        ("信義區", 25.0339, 121.5645),
    ]
    
    print(f"\n📍 測試不同地點 (半徑 1 公里)\n")
    
    for name, lat, lon in locations:
        results = service.search_nearby_updates(lat, lon, 1.0)
        print(f"{name:12s}: 找到 {len(results):>3} 筆都市更新案件")


if __name__ == "__main__":
    print("=" * 60)
    print("🏗️  測試都市更新附近搜索功能")
    print("=" * 60)
    
    test_nearby_search()
    test_different_locations()
    
    print("\n" + "=" * 60)
    print("✨ 測試完成")
    print("=" * 60)
