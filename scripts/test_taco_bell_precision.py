#!/usr/bin/env python3
"""
Test the improved scraper precision for Taco Bell detection
"""

import sys
sys.path.append('.')
from uk_service_stations import MasterStationsScraper

def test_taco_bell_precision():
    scraper = MasterStationsScraper()
    
    # Test URLs: one WITH Taco Bell, one WITHOUT Taco Bell
    test_cases = [
        {
            'url': 'https://welcomebreak.co.uk/locations/corley/',
            'expected': True,  # Should find Taco Bell here
            'name': 'Corley (HAS Taco Bell)'
        },
        {
            'url': 'https://welcomebreak.co.uk/locations/abington/',
            'expected': False,  # Should NOT find Taco Bell here
            'name': 'Abington (NO Taco Bell)'
        }
    ]
    
    print("🧪 Testing Taco Bell Detection Precision")
    print("=" * 50)
    
    for test_case in test_cases:
        print(f"\n🔍 Testing: {test_case['name']}")
        print(f"URL: {test_case['url']}")
        
        try:
            facilities = scraper.scrape_facilities_enhanced(test_case['url'], test_case['name'])
            if facilities:
                food_outlets = facilities.get('food_outlets', [])
                has_taco_bell = 'Taco Bell' in food_outlets
                
                print(f"Food outlets found: {food_outlets}")
                print(f"Taco Bell detected: {has_taco_bell}")
                print(f"Expected: {test_case['expected']}")
                
                if has_taco_bell == test_case['expected']:
                    print("✅ CORRECT - Test PASSED")
                else:
                    print("❌ INCORRECT - Test FAILED")
                    if has_taco_bell and not test_case['expected']:
                        print("   FALSE POSITIVE: Found Taco Bell where it shouldn't be")
                    elif not has_taco_bell and test_case['expected']:
                        print("   FALSE NEGATIVE: Didn't find Taco Bell where it should be")
            else:
                print("❌ Scraping failed")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("-" * 30)

if __name__ == "__main__":
    test_taco_bell_precision()