#!/usr/bin/env python3
"""
Test the precision fix for brand detection
"""

import sys
sys.path.append('.')
from uk_service_stations import MasterStationsScraper

def test_precision_fix():
    scraper = MasterStationsScraper()
    
    # Test a few stations that were showing false positive Spar
    test_urls = [
        "https://extraservices.co.uk/locations/baldock",
        "https://moto-way.com/services/birch-eastbound/",
        "https://gloucesterservices.com/"
    ]
    
    for url in test_urls:
        print(f"\n🔍 Testing: {url}")
        print("=" * 60)
        
        try:
            facilities = scraper.scrape_facilities_enhanced(url, "Test")
            if facilities:
                retail_shops = facilities.get('retail_shops', [])
                print(f"✅ Retail shops found: {retail_shops}")
                if 'Spar' in retail_shops:
                    print("❌ Still detecting Spar - needs more fixing")
                else:
                    print("✅ Spar false positive fixed!")
            else:
                print("❌ Scraping failed")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_precision_fix()