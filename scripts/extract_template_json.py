#!/usr/bin/env python3
"""
Extract JSON data from template tags and query for food stores
"""

import requests
import json
import re
from bs4 import BeautifulSoup

def extract_complete_json_from_string(partial_json, full_content):
    """
    Try to extract complete JSON from a partial match by finding the context in the full content
    """
    # Find where this partial JSON appears in the full content
    start_pos = full_content.find(partial_json)
    if start_pos == -1:
        return None
    
    # Look backwards to find the opening brace
    search_start = start_pos
    while search_start > 0 and full_content[search_start] != '{':
        search_start -= 1
    
    if search_start == 0:
        return None
    
    # Count braces to find the complete JSON object
    brace_count = 0
    current_pos = search_start
    json_end = -1
    
    while current_pos < len(full_content):
        char = full_content[current_pos]
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                json_end = current_pos + 1
                break
        current_pos += 1
    
    if json_end > 0:
        return full_content[search_start:json_end]
    return None

def extract_template_json(url):
    """
    Find template tags with JSON and extract food store information
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f"Extracting template JSON from: {url}")
    print("=" * 60)
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Method 1: Look for template tags with :template attribute
        template_elements = soup.find_all(attrs={"template": True})
        if template_elements:
            print(f"Found {len(template_elements)} elements with template attribute")
            
        # Method 2: Look for elements containing ":template=" in their attributes or content
        all_elements = soup.find_all()
        template_candidates = []
        
        for element in all_elements:
            # Check if any attribute contains "template"
            for attr_name, attr_value in element.attrs.items():
                if "template" in attr_name.lower() or (isinstance(attr_value, str) and "template" in attr_value.lower()):
                    template_candidates.append(element)
                    print(f"Found template in {element.name} attribute {attr_name}: {str(attr_value)[:100]}...")
                    break
            
            # Also check element content for :template=
            if element.string and ":template=" in str(element.string):
                template_candidates.append(element)
                print(f"Found ':template=' in {element.name} content: {str(element.string)[:100]}...")
        
        if template_candidates:
            print(f"Found {len(template_candidates)} template candidate elements")
        
        # Method 3: Look for script tags or text content containing JSON with template references
        page_content = response.text
        
        # Search for patterns like :template= followed by JSON - more flexible pattern
        template_patterns = []
        
        # Look for :template="..." attribute values that might contain complete JSON
        template_match = re.search(r':template\s*=\s*"([^"]*)"', page_content, re.IGNORECASE | re.DOTALL)
        if template_match:
            template_value = template_match.group(1)
            # Decode HTML entities
            template_value = template_value.replace('&quot;', '"').replace('&#x27;', "'").replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            template_patterns.append(template_value)
            print(f"Found template attribute with {len(template_value)} characters")
        
        # Also look for simple patterns
        simple_patterns = re.findall(r':template[^{]*(\{.*?\})', page_content, re.IGNORECASE)
        template_patterns.extend(simple_patterns)
        
        if template_patterns:
            print(f"Found {len(template_patterns)} template patterns with JSON")
            for i, pattern in enumerate(template_patterns[:3]):  # Show first 3
                print(f"  Pattern {i+1}: {pattern[:200]}...")
                
                # Try to extract food stores from each pattern
                try:
                    data = json.loads(pattern)
                    stores = extract_food_from_parsed_json(data)
                    if stores:
                        print(f"    ✅ Found {len(stores)} stores in this pattern")
                        return stores
                except json.JSONDecodeError as e:
                    print(f"    ❌ Pattern {i+1} is not valid JSON: {str(e)[:50]}...")
                    
                    # Try to fix common JSON issues
                    try:
                        # Try to extract a more complete JSON by counting braces
                        fixed_json = extract_complete_json_from_string(pattern, page_content)
                        if fixed_json and fixed_json != pattern:
                            print(f"    🔧 Trying to fix JSON...")
                            data = json.loads(fixed_json)
                            stores = extract_food_from_parsed_json(data)
                            if stores:
                                print(f"    ✅ Fixed JSON contains {len(stores)} stores!")
                                return stores
                    except json.JSONDecodeError:
                        continue
        
        # Method 3b: Look for broader template patterns
        broader_patterns = re.findall(r'template[^{]*(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})', page_content, re.IGNORECASE)
        if broader_patterns:
            print(f"Found {len(broader_patterns)} broader template patterns")
            for i, pattern in enumerate(broader_patterns[:3]):
                print(f"  Broader pattern {i+1}: {pattern[:200]}...")
        
        # Method 3c: Look for any wrapper containing template and JSON
        wrapper_patterns = re.findall(r'<[^>]*template[^>]*>.*?(\{.*?\})', page_content, re.IGNORECASE | re.DOTALL)
        if wrapper_patterns:
            print(f"Found {len(wrapper_patterns)} wrapper patterns with JSON")
            for i, pattern in enumerate(wrapper_patterns[:3]):
                print(f"  Wrapper pattern {i+1}: {pattern[:200]}...")
                try:
                    data = json.loads(pattern)
                    stores = extract_food_from_parsed_json(data)
                    if stores:
                        print(f"    ✅ Found {len(stores)} stores in wrapper pattern")
                        return stores
                except json.JSONDecodeError:
                    continue
            
        # Method 4: Search for brands JSON (priority method since we know it exists)
        scripts = soup.find_all('script')
        print(f"Scanning {len(scripts)} script tags for brands JSON...")
        
        for i, script in enumerate(scripts):
            if script.string and len(script.string.strip()) > 0:
                print(f"  Script {i+1}: {len(script.string)} characters")
                
                # Look for the specific brands JSON structure we've seen before
                if '"type":"brands"' in script.string:
                    print(f"    ✅ Found brands JSON in script {i+1}!")
                    brands_start = script.string.find('"type":"brands"')
                    
                    # Find the complete JSON object
                    search_start = brands_start
                    while search_start > 0 and script.string[search_start] != '{':
                        search_start -= 1
                    
                    # Count braces to find complete object
                    brace_count = 0
                    current_pos = search_start
                    json_end = -1
                    
                    while current_pos < len(script.string):
                        char = script.string[current_pos]
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                json_end = current_pos + 1
                                break
                        current_pos += 1
                    
                    if json_end > 0:
                        brands_json = script.string[search_start:json_end]
                        print(f"    Extracted brands JSON: {len(brands_json)} characters")
                        return extract_food_stores_from_json(brands_json)
                    else:
                        print(f"    ❌ Could not find complete JSON object")
                
                # Also check if this script contains template references
                if ":template=" in script.string or "template" in script.string.lower():
                    print(f"    📍 Script {i+1} contains template references")
                    # Look for JSON objects in this script
                    json_objects = re.findall(r'\{[^{}]*(?:"type"|"brands"|"food"|"restaurants"|"stores")[^{}]*\}', script.string)
                    if json_objects:
                        print(f"      Found {len(json_objects)} JSON objects with relevant keys")
                        for j, obj in enumerate(json_objects):
                            try:
                                data = json.loads(obj)
                                stores = extract_food_from_parsed_json(data)
                                if stores:
                                    print(f"        ✅ JSON object {j+1} contains {len(stores)} stores")
                                    return stores
                            except json.JSONDecodeError:
                                continue
        
        # Method 5: Look for JSON objects that might contain food/brand information
        # Find all potential JSON objects in script tags or data attributes
        potential_json = []
        
        # Search in script tags for any JSON with relevant keys
        for script in scripts:
            if script.string:
                # Look for JSON objects that might contain brands/food info
                json_matches = re.findall(r'\{[^{}]*(?:"type"|"brands"|"food"|"restaurants"|"stores")[^{}]*\}', script.string)
                potential_json.extend(json_matches)
        
        # If no specific brands JSON found, try parsing all potential JSON
        food_stores = []
        for json_str in potential_json:
            try:
                data = json.loads(json_str)
                stores = extract_food_from_parsed_json(data)
                food_stores.extend(stores)
            except json.JSONDecodeError:
                continue
        
        if food_stores:
            return food_stores
        else:
            print("❌ No food store data found in JSON structures")
            return []
            
    except requests.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
        return []

def extract_food_stores_from_json(json_str):
    """
    Extract food stores from a JSON string
    """
    try:
        data = json.loads(json_str)
        print(f"✅ Successfully parsed JSON with type: {data.get('type')}")
        
        return extract_food_from_parsed_json(data)
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {str(e)}")
        return []

def extract_food_from_parsed_json(data):
    """
    Extract food stores from parsed JSON data
    """
    food_stores = []
    
    # Handle the brands JSON structure we've seen
    if isinstance(data, dict) and data.get('type') == 'brands':
        value = data.get('value', {})
        items = value.get('items', [])
        
        print(f"Processing {len(items)} brand items...")
        
        for item in items:
            title = item.get('title', '').strip()
            available = item.get('available', True)
            
            if available and title:
                # Check if this is likely a food store
                if is_food_store(title):
                    food_stores.append({
                        'name': title,
                        'available': available,
                        'category': 'food'
                    })
                else:
                    # Include all brands but categorize them
                    category = categorize_brand(title)
                    food_stores.append({
                        'name': title,
                        'available': available,
                        'category': category
                    })
    
    # Handle location JSON with scroller containing facilities
    elif isinstance(data, dict) and data.get('type') == 'location':
        print("Processing location JSON structure...")
        value = data.get('value', {})
        scroller = value.get('scroller', [])
        
        print(f"Found {len(scroller)} sections in scroller...")
        
        for section in scroller:
            if isinstance(section, dict):
                section_type = section.get('type', '')
                print(f"  Processing section type: {section_type}")
                
                # Look for facilities section
                if section_type == 'facilities':
                    facilities_value = section.get('value', {})
                    items = facilities_value.get('items', [])
                    
                    print(f"    Found {len(items)} facility items")
                    for item in items:
                        if isinstance(item, dict):
                            title = item.get('title', '') or ''
                            content = item.get('content', '') or ''
                            
                            if isinstance(title, str):
                                title = title.strip()
                            else:
                                title = str(title).strip() if title else ''
                            
                            if isinstance(content, str):
                                content = content.strip()
                            else:
                                content = str(content).strip() if content else ''
                            
                            if title:
                                category = categorize_brand(title)
                                food_stores.append({
                                    'name': title,
                                    'available': True,
                                    'category': category,
                                    'description': content
                                })
                
                # Look for brands section (might be nested)
                elif section_type == 'brands':
                    brands_value = section.get('value', {})
                    items = brands_value.get('items', [])
                    
                    print(f"    Found {len(items)} brand items")
                    for item in items:
                        if isinstance(item, dict):
                            title = item.get('title', '') or ''
                            available = item.get('available', True)
                            
                            if isinstance(title, str):
                                title = title.strip()
                            else:
                                title = str(title).strip() if title else ''
                            
                            if available and title:
                                category = categorize_brand(title)
                                food_stores.append({
                                    'name': title,
                                    'available': available,
                                    'category': category
                                })
                
                # Recursively process nested structures
                elif 'value' in section:
                    nested_stores = extract_food_from_parsed_json(section)
                    food_stores.extend(nested_stores)
    
    # Handle other JSON structures that might contain store info
    elif isinstance(data, dict):
        # Look for arrays of items/stores/brands
        for key, value in data.items():
            if isinstance(value, list) and key.lower() in ['items', 'stores', 'brands', 'facilities', 'outlets']:
                for item in value:
                    if isinstance(item, dict) and 'title' in item:
                        name = item['title'].strip()
                        if name:
                            category = categorize_brand(name)
                            food_stores.append({
                                'name': name,
                                'available': item.get('available', True),
                                'category': category
                            })
                    elif isinstance(item, dict) and 'name' in item:
                        name = item['name'].strip()
                        if name:
                            category = categorize_brand(name)
                            food_stores.append({
                                'name': name,
                                'available': item.get('available', True),
                                'category': category
                            })
            
            # Recursively process nested objects
            elif isinstance(value, dict):
                nested_stores = extract_food_from_parsed_json(value)
                food_stores.extend(nested_stores)
            
            # Process arrays of objects
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        nested_stores = extract_food_from_parsed_json(item)
                        food_stores.extend(nested_stores)
    
    return food_stores

def is_food_store(name):
    """
    Determine if a brand/store is food-related
    """
    food_keywords = [
        'coffee', 'cafe', 'restaurant', 'food', 'kitchen', 'grill', 'pizza', 
        'burger', 'sandwich', 'noodle', 'chicken', 'bakery', 'deli', 'bar',
        'bistro', 'eatery', 'takeaway', 'fast food', 'dining', 'fresh'
    ]
    
    food_brands = [
        'costa', 'starbucks', 'mcdonalds', "mcdonald's", 'burger king', 'kfc', 'subway',
        'greggs', 'pret', 'leon', 'wasabi', 'itsu', 'chozen noodle', 'coco',
        'krispy kreme', 'dunkin', 'tesco', 'fresh food cafe', 'upper crust',
        'cornish bakery', 'pasty shop'
    ]
    
    name_lower = name.lower()
    
    # Check for food keywords
    for keyword in food_keywords:
        if keyword in name_lower:
            return True
    
    # Check for known food brands
    for brand in food_brands:
        if brand in name_lower:
            return True
    
    return False

def categorize_brand(name):
    """
    Categorize a brand into food, retail, service, etc.
    """
    if is_food_store(name):
        return 'food'
    
    retail_keywords = ['shop', 'store', 'mart', 'whsmith', 'wh smith', 'boots', 'travel']
    service_keywords = ['fuel', 'petrol', 'diesel', 'service', 'car wash', 'atm']
    
    name_lower = name.lower()
    
    for keyword in retail_keywords:
        if keyword in name_lower:
            return 'retail'
    
    for keyword in service_keywords:
        if keyword in name_lower:
            return 'service'
    
    return 'other'

def main():
    """
    Main function to test the extraction
    """
    # Test with Watford Gap
    url = "https://www.roadchef.com/motorway-services/watford-gap"
    
    food_stores = extract_template_json(url)
    
    if food_stores:
        print(f"\n✅ Found {len(food_stores)} items:")
        print("=" * 60)
        
        # Group by category
        categories = {}
        for store in food_stores:
            category = store['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(store)
        
        # Display results
        for category, stores in categories.items():
            print(f"\n{category.upper()} ({len(stores)} items):")
            for store in stores:
                availability = "✅" if store['available'] else "❌"
                print(f"  {availability} {store['name']}")
        
        # Focus on food stores
        food_only = [store for store in food_stores if store['category'] == 'food']
        if food_only:
            print(f"\n🍔 FOOD STORES ONLY ({len(food_only)} items):")
            for store in food_only:
                availability = "✅" if store['available'] else "❌"
                print(f"  {availability} {store['name']}")
    else:
        print("❌ No food stores found")

if __name__ == "__main__":
    main()