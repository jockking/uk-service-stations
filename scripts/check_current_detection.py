#!/usr/bin/env python3
"""
Check what the current scraper actually detects at Watford Gap
"""

import sys
sys.path.append('.')
from uk_service_stations import MasterStationsScraper

def check_current_detection():
    scraper = MasterStationsScraper()
    
    url = "https://www.roadchef.com/motorway-services/watford-gap"
    
    print("Testing current scraper detection at Watford Gap...")
    print("=" * 60)
    
    facilities = scraper.scrape_facilities_enhanced(url, "RoadChef")
    
    if facilities:
        print("✅ Scraping completed")
        print()
        print("DETECTED FACILITIES:")
        print(f"🍔 Food outlets ({len(facilities['food_outlets'])}): {facilities['food_outlets']}")
        print(f"🛍️ Retail shops ({len(facilities['retail_shops'])}): {facilities['retail_shops']}")
        print(f"🏢 Amenities ({len(facilities['amenities'])}): {facilities['amenities']}")
        print(f"🔧 Services ({len(facilities['services'])}): {facilities['services']}")
        
        total = (len(facilities['food_outlets']) + len(facilities['retail_shops']) + 
                len(facilities['amenities']) + len(facilities['services']))
        print(f"\n📊 Total facilities: {total}")
        
        if total == 0:
            print("\n❌ No facilities detected - this confirms the JavaScript rendering issue")
        
    else:
        print("❌ Scraping failed")

if __name__ == "__main__":
    check_current_detection()