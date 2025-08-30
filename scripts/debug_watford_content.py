#!/usr/bin/env python3
"""
Debug what content we're actually getting from Watford Gap
"""

import requests
from bs4 import BeautifulSoup

def debug_watford_content():
    url = "https://www.roadchef.com/motorway-services/watford-gap"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print("Debugging Watford Gap content extraction...")
    print("=" * 60)
    
    response = requests.get(url, headers=headers, timeout=20)
    print(f"Response status: {response.status_code}")
    print(f"Response content length: {len(response.content)}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Check total page content
    page_text = soup.get_text()
    print(f"Page text length: {len(page_text)}")
    
    # Check if we have the brands we expect in the plain text
    expected_brands = ['Costa Coffee', 'WHSmith', 'Chozen Noodle', 'Coco', 'Krispy Kreme', 'Fresh Food Cafe']
    
    print("\nBrands in page text:")
    for brand in expected_brands:
        if brand.lower() in page_text.lower():
            print(f"✅ Found '{brand}' in page text")
        else:
            print(f"❌ '{brand}' not found in page text")
    
    # Check script tags
    scripts = soup.find_all('script')
    print(f"\nTotal script tags: {len(scripts)}")
    
    total_script_content = ""
    for i, script in enumerate(scripts):
        if script.string:
            content = script.string
            total_script_content += content + " "
            print(f"Script {i+1}: {len(content)} characters")
            
            # Check if this script contains brands
            if '"type":"brands"' in content:
                print(f"  ✅ Contains brands JSON!")
                # Show snippet
                brands_start = content.find('"type":"brands"')
                snippet_start = max(0, brands_start - 50)
                snippet_end = min(len(content), brands_start + 200)
                print(f"  Snippet: ...{content[snippet_start:snippet_end]}...")
            
            # Check for brand names in scripts
            brands_found = []
            for brand in expected_brands:
                if brand.lower() in content.lower():
                    brands_found.append(brand)
            
            if brands_found:
                print(f"  📍 Contains brands: {brands_found}")
    
    print(f"\nTotal script content length: {len(total_script_content)}")
    
    # Check if brands are in the combined script content
    print(f"Brands in combined script content: {'type\":\"brands' in total_script_content}")
    
    # Look for any JSON-like structures
    import re
    json_patterns = re.findall(r'\{[^{}]*"type"[^{}]*\}', total_script_content)
    print(f"\nFound {len(json_patterns)} JSON patterns with 'type' field")
    
    for i, pattern in enumerate(json_patterns[:3]):  # Show first 3
        print(f"Pattern {i+1}: {pattern[:100]}...")

if __name__ == "__main__":
    debug_watford_content()