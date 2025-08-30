#!/usr/bin/env python3
"""
Debug the JSON brands extraction method
"""

import requests
import json
from bs4 import BeautifulSoup

def debug_json_extraction():
    url = "https://www.roadchef.com/motorway-services/watford-gap"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print("Debugging JSON brands extraction...")
    print("=" * 60)
    
    response = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract script content (original case)
    script_text_original = ""
    for script in soup.find_all('script'):
        if script.string:
            script_text_original += script.string + " "
    
    print(f"Script content length: {len(script_text_original)}")
    
    # Test the extraction logic step by step
    print(f"Contains 'type\":\"brands': {'\"type\":\"brands\"' in script_text_original}")
    
    if '"type":"brands"' in script_text_original:
        print("✅ Found brands type in script")
        
        # Find the brands JSON object
        brands_start = script_text_original.find('"type":"brands"')
        print(f"Brands start position: {brands_start}")
        
        # Find the complete JSON object by counting braces
        # Go back to find opening brace
        search_start = brands_start
        while search_start > 0 and script_text_original[search_start] != '{':
            search_start -= 1
        
        print(f"JSON start position: {search_start}")
        
        # Count braces to find complete object
        brace_count = 0
        current_pos = search_start
        json_end = -1
        
        while current_pos < len(script_text_original):
            char = script_text_original[current_pos]
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    json_end = current_pos + 1
                    break
            current_pos += 1
        
        if json_end > 0:
            brands_json = script_text_original[search_start:json_end]
            print(f"Extracted JSON length: {len(brands_json)}")
            print(f"JSON snippet: {brands_json[:200]}...")
            
            try:
                brands_data = json.loads(brands_json)
                print("✅ JSON parsing successful!")
                print(f"JSON type: {brands_data.get('type')}")
                
                if 'value' in brands_data:
                    value = brands_data['value']
                    print(f"Value keys: {list(value.keys()) if isinstance(value, dict) else 'Not a dict'}")
                    
                    if 'items' in value:
                        items = value['items']
                        print(f"Number of items: {len(items)}")
                        
                        for i, item in enumerate(items[:3]):  # Show first 3
                            title = item.get('title', 'No title')
                            available = item.get('available', False)
                            print(f"  Item {i+1}: {title} (available: {available})")
                            
                        # Test the extraction logic
                        extracted_brands = []
                        for item in items:
                            title = item.get('title', '')
                            available = item.get('available', True)
                            
                            if available and title:
                                clean_title = title.strip()
                                if clean_title:
                                    extracted_brands.append(clean_title)
                        
                        print(f"Extracted brands: {extracted_brands}")
                        
                else:
                    print("❌ No 'value' key in JSON")
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {str(e)}")
                print(f"JSON content: {brands_json}")
        else:
            print("❌ Could not find JSON end")
    else:
        print("❌ No brands type found in script")

if __name__ == "__main__":
    debug_json_extraction()