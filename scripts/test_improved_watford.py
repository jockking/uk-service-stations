#!/usr/bin/env python3
"""
Test the improved scraper with JSON brands parsing on Watford Gap
"""

import sys
sys.path.append('.')
from uk_service_stations import MasterStationsScraper

def test_improved_watford():
    scraper = MasterStationsScraper()
    
    url = "https://www.roadchef.com/motorway-services/watford-gap"
    
    print("Testing improved scraper with JSON brands parsing...")
    print(f"URL: {url}")
    print("=" * 60)
    
    facilities = scraper.scrape_facilities_enhanced(url, "RoadChef")
    
    if facilities:
        print("✅ Scraping completed!")
        print()
        print("RESULTS:")
        print(f"🍔 Food outlets: {facilities['food_outlets']}")
        print(f"🛍️  Retail shops: {facilities['retail_shops']}")
        print(f"🏢 Amenities: {facilities['amenities']}")
        print(f"🔧 Services: {facilities['services']}")
        
        total_facilities = (len(facilities['food_outlets']) + 
                          len(facilities['retail_shops']) + 
                          len(facilities['amenities']) + 
                          len(facilities['services']))
        
        print()
        print(f"📊 Total facilities detected: {total_facilities}")
        
        # Check for expected brands
        expected_brands = ['Costa Coffee', 'WHSmith', 'Chozen Noodle', 'Coco', 'Krispy Kreme', 'Fresh Food Cafe']
        all_found_brands = facilities['food_outlets'] + facilities['retail_shops']
        
        print()
        print("BRAND VERIFICATION:")
        print("-" * 30)
        for expected in expected_brands:
            # Check for partial matches too
            found = any(expected.lower() in brand.lower() for brand in all_found_brands)
            exact_match = expected in all_found_brands
            
            if exact_match:
                print(f"✅ {expected} (exact match)")
            elif found:
                matching_brand = next(brand for brand in all_found_brands if expected.lower() in brand.lower())
                print(f"✅ {expected} → found as '{matching_brand}'")
            else:
                print(f"❌ {expected} (not found)")
        
        # Show any additional brands found
        additional_brands = [brand for brand in all_found_brands 
                           if not any(expected.lower() in brand.lower() for expected in expected_brands)]
        if additional_brands:
            print(f"\n🔍 Additional brands found: {additional_brands}")
        
    else:
        print("❌ Scraping failed")

if __name__ == "__main__":
    test_improved_watford()