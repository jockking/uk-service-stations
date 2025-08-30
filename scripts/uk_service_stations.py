#!/usr/bin/env python3
"""
Master Stations Scraper
========================
Efficient scraper using the master_service_stations.json file as the definitive source.
No more CSV downloads or URL discovery - just direct scraping from known URLs.
"""

import requests
import json
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup

class MasterStationsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Load master stations file
        self.master_stations = self.load_master_stations()
        
        # Manual overrides for JavaScript-heavy sites where brands can't be scraped
        self.manual_overrides = {
            'Watford Gap Services M1': {
                'food_outlets': ['Costa Coffee', 'Costa Drive Thru', "McDonald's", 'Fresh Food Cafe', 'Chozen Noodle', 'Coco Di Mama', 'Krispy Kreme'],
                'retail_shops': ['WHSmith'],
                'reason': 'JavaScript-heavy RoadChef site - brands extracted from template JSON'
            }
        }

    def load_master_stations(self):
        """Load the master stations file"""
        try:
            with open('../data/master_service_stations.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            stations = data['stations']
            print(f"📂 Loaded {len(stations)} stations from master file")
            print(f"🔗 {len([s for s in stations if s['website_url']])} stations have URLs")
            
            return stations
        except FileNotFoundError:
            print("❌ Master stations file not found. Please run create_master_stations.py first.")
            return []
        except Exception as e:
            print(f"❌ Error loading master stations: {str(e)}")
            return []

    def extract_json_brands(self, script_content):
        """Extract brands from JSON structures like {"type":"brands"}"""
        try:
            # Look for brands JSON structure
            if '"type":"brands"' not in script_content:
                return []
            
            # Find the brands JSON object
            brands_start = script_content.find('"type":"brands"')
            if brands_start == -1:
                return []
            
            # Find the complete JSON object by counting braces
            # Go back to find opening brace
            search_start = brands_start
            while search_start > 0 and script_content[search_start] != '{':
                search_start -= 1
            
            # Count braces to find complete object
            brace_count = 0
            current_pos = search_start
            
            while current_pos < len(script_content):
                char = script_content[current_pos]
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        brands_json = script_content[search_start:current_pos + 1]
                        break
                current_pos += 1
            else:
                return []
            
            # Parse the JSON
            brands_data = json.loads(brands_json)
            
            if (brands_data.get('type') == 'brands' and 
                'value' in brands_data and 
                'items' in brands_data['value']):
                
                items = brands_data['value']['items']
                extracted_brands = []
                
                for item in items:
                    title = item.get('title', '')
                    available = item.get('available', True)  # Default to available
                    
                    if available and title:
                        # Clean up brand name
                        clean_title = title.strip()
                        if clean_title:
                            extracted_brands.append(clean_title)
                
                return extracted_brands
            
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            # Silently fail - this is expected for most sites
            pass
        
        return []

    def extract_template_json(self, soup, page_content):
        """Extract brands from template wrapper elements with JSON content"""
        try:
            # Look for elements with :template attributes containing JSON
            template_elements = soup.find_all()
            for element in template_elements:
                for attr_name, attr_value in element.attrs.items():
                    if "template" in attr_name.lower() and isinstance(attr_value, str):
                        # Try to decode HTML entities and parse as JSON
                        template_value = attr_value.replace('&quot;', '"').replace('&#x27;', "'").replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                        
                        try:
                            data = json.loads(template_value)
                            return self.extract_brands_from_template_json(data)
                        except json.JSONDecodeError:
                            # Try to extract complete JSON from page content
                            complete_json = self.extract_complete_json_from_content(template_value, page_content)
                            if complete_json:
                                try:
                                    data = json.loads(complete_json)
                                    return self.extract_brands_from_template_json(data)
                                except json.JSONDecodeError:
                                    continue
            
            # Also look for template patterns in page content
            import re
            template_match = re.search(r':template\s*=\s*"([^"]*)"', page_content, re.IGNORECASE | re.DOTALL)
            if template_match:
                template_value = template_match.group(1)
                template_value = template_value.replace('&quot;', '"').replace('&#x27;', "'").replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                
                try:
                    data = json.loads(template_value)
                    return self.extract_brands_from_template_json(data)
                except json.JSONDecodeError:
                    complete_json = self.extract_complete_json_from_content(template_value, page_content)
                    if complete_json:
                        try:
                            data = json.loads(complete_json)
                            return self.extract_brands_from_template_json(data)
                        except json.JSONDecodeError:
                            pass
        
        except Exception:
            pass
        
        return []

    def extract_complete_json_from_content(self, partial_json, full_content):
        """Extract complete JSON from partial match in full content"""
        try:
            start_pos = full_content.find(partial_json)
            if start_pos == -1:
                return None
            
            # Find opening brace
            search_start = start_pos
            while search_start > 0 and full_content[search_start] != '{':
                search_start -= 1
            
            if search_start == 0:
                return None
            
            # Count braces to find complete object
            brace_count = 0
            current_pos = search_start
            
            while current_pos < len(full_content):
                char = full_content[current_pos]
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        return full_content[search_start:current_pos + 1]
                current_pos += 1
        except Exception:
            pass
        
        return None

    def extract_brands_from_template_json(self, data):
        """Extract brands from template JSON data structures"""
        brands = []
        
        try:
            # Handle location JSON with scroller
            if isinstance(data, dict) and data.get('type') == 'location':
                value = data.get('value', {})
                scroller = value.get('scroller', [])
                
                for section in scroller:
                    if isinstance(section, dict):
                        section_type = section.get('type', '')
                        
                        # Process facilities section
                        if section_type == 'facilities':
                            facilities_value = section.get('value', {})
                            items = facilities_value.get('items', [])
                            
                            for item in items:
                                if isinstance(item, dict):
                                    title = item.get('title', '') or ''
                                    if isinstance(title, str):
                                        title = title.strip()
                                    elif title:
                                        title = str(title).strip()
                                    
                                    if title and self.is_brand_name(title):
                                        brands.append(title)
                        
                        # Process brands section
                        elif section_type == 'brands':
                            brands_value = section.get('value', {})
                            items = brands_value.get('items', [])
                            
                            for item in items:
                                if isinstance(item, dict):
                                    title = item.get('title', '') or ''
                                    available = item.get('available', True)
                                    
                                    if isinstance(title, str):
                                        title = title.strip()
                                    elif title:
                                        title = str(title).strip()
                                    
                                    if available and title:
                                        brands.append(title)
            
            # Handle direct brands JSON
            elif isinstance(data, dict) and data.get('type') == 'brands':
                value = data.get('value', {})
                items = value.get('items', [])
                
                for item in items:
                    title = item.get('title', '') or ''
                    available = item.get('available', True)
                    
                    if isinstance(title, str):
                        title = title.strip()
                    elif title:
                        title = str(title).strip()
                    
                    if available and title:
                        brands.append(title)
        
        except Exception:
            pass
        
        return brands

    def is_brand_name(self, name):
        """Check if a name is likely a brand rather than a facility"""
        # Skip generic facilities
        generic_facilities = [
            'parking', 'toilet', 'wifi', 'wi-fi', 'fuel', 'petrol', 'diesel',
            'baby changing', 'wheelchair accessible', 'disabled access', 
            'ev charging', 'charging', 'shower', 'cash machine', 'atm',
            'open 24', '24 hours', 'free water', 'order ahead', 'pet friendly',
            'car wash', 'medium power', 'high power', 'charging point',
            'charging hub', 'cars and small vans', 'caravans', 'hgv'
        ]
        
        name_lower = name.lower()
        for facility in generic_facilities:
            if facility in name_lower:
                return False
        
        # If it contains brand-like keywords, it's probably a brand
        brand_keywords = [
            'coffee', 'cafe', 'restaurant', 'food', 'kitchen', 'grill', 'pizza', 
            'burger', 'sandwich', 'noodle', 'chicken', 'bakery', 'shop', 'store',
            'smith', 'express', 'fresh', 'costa', 'mcdonald', 'krispy', 'chozen', 'coco'
        ]
        
        for keyword in brand_keywords:
            if keyword in name_lower:
                return True
        
        return False

    def scrape_facilities_enhanced(self, url, operator):
        """Enhanced facility scraping with comprehensive brand detection"""
        try:
            # Try with different headers to avoid blocking
            response = self.session.get(url, timeout=20, allow_redirects=True)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Debug: Check if we got minimal content (JavaScript-heavy sites)
            page_length = len(response.content)
            if page_length < 10000:  # Very small page, likely minimal HTML
                print(f"    ⚠️  Minimal content detected ({page_length} bytes), may be JavaScript-heavy")
            
            # Comprehensive brand mapping
            brand_mapping = {
                # Food outlets
                'burger king': 'Burger King',
                'mcdonalds': "McDonald's",
                'mcdonald\'s': "McDonald's",
                'kfc': 'KFC',
                'kentucky fried chicken': 'KFC',
                'subway': 'Subway',
                'costa coffee': 'Costa Coffee',
                'costa': 'Costa Coffee',
                'starbucks': 'Starbucks',
                'starbucks coffee': 'Starbucks',
                'greggs': 'Greggs',
                'gregg': 'Greggs',
                'greggs bakery': 'Greggs',
                'greggs the bakery': 'Greggs',
                'krispy kreme': 'Krispy Kreme',
                'krispy kremes': 'Krispy Kreme',
                'krispy-kreme': 'Krispy Kreme',
                'pret a manger': 'Pret A Manger',
                'pret': 'Pret A Manger',
                'leon': 'Leon',
                'leon restaurants': 'Leon',
                'pizza express': 'Pizza Express',
                'nandos': "Nando's",
                'nando\'s': "Nando's",
                'chopstix': 'Chopstix',
                'taco bell': 'Taco Bell',
                'upper crust': 'Upper Crust',
                'the good breakfast': 'The Good Breakfast',
                'chozen noodle': 'Chozen Noodle',
                'coco di mama': 'Coco Di Mama',
                'coco': 'Coco Di Mama',
                'fresh food cafe': 'Fresh Food Cafe',
                'costa drive thru': 'Costa Drive Thru',
                
                # Retail shops
                'whsmith': 'WHSmith',
                'wh smith': 'WHSmith',
                'marks & spencer': 'Marks & Spencer',
                'marks and spencer': 'Marks & Spencer',
                'm&s': 'Marks & Spencer',
                'waitrose': 'Waitrose & Partners',
                'waitrose & partners': 'Waitrose & Partners',
                'boots': 'Boots',
                'tesco': 'Tesco Express',
                'tesco express': 'Tesco Express',
                'spar': 'Spar'
            }
            
            facilities = {
                'food_outlets': [],
                'retail_shops': [],
                'amenities': [],
                'services': []
            }
            
            # Extract all text content
            page_text = soup.get_text().lower()
            
            # Also extract from script tags (JSON-LD, etc.)
            script_text = ""
            script_text_original = ""  # Keep original case for JSON parsing
            for script in soup.find_all('script'):
                if script.string:
                    script_text += script.string.lower() + " "
                    script_text_original += script.string + " "
            
            # Combine all text sources
            all_text = page_text + " " + script_text
            
            # Enhanced brand detection from all sources
            found_brands = set()
            for search_term, brand_name in brand_mapping.items():
                if search_term in all_text:
                    found_brands.add(brand_name)
            
            # SPECIAL: Parse JSON brands data (for RoadChef and similar sites)
            json_brands = self.extract_json_brands(script_text_original)
            if json_brands:
                print(f"    🎯 Found JSON brands data: {len(json_brands)} brands")
                found_brands.update(json_brands)
            
            # SPECIAL: Parse template JSON data (for RoadChef template wrapper elements)
            template_brands = self.extract_template_json(soup, response.text)
            if template_brands:
                print(f"    📋 Found template JSON brands: {len(template_brands)} brands")
                found_brands.update(template_brands)
            
            # Check in meta tags, alt texts, and specific elements
            for element in soup.find_all(['img', 'a', 'div', 'span', 'li', 'p'], alt=True):
                alt_text = element.get('alt', '').lower()
                for search_term, brand_name in brand_mapping.items():
                    if search_term in alt_text:
                        found_brands.add(brand_name)
            
            # Check element text content and class names
            for element in soup.find_all(['div', 'span', 'li', 'p', 'h1', 'h2', 'h3', 'h4']):
                element_text = element.get_text().lower()
                class_names = ' '.join(element.get('class', [])).lower()
                
                for search_term, brand_name in brand_mapping.items():
                    if search_term in element_text or search_term in class_names:
                        found_brands.add(brand_name)
            
            # Categorize brands
            food_outlets = [
                'Burger King', "McDonald's", 'KFC', 'Subway', 'Costa Coffee', 'Starbucks',
                'Greggs', 'Krispy Kreme', 'Pret A Manger', 'Leon', 'Pizza Express',
                "Nando's", 'Chopstix', 'Taco Bell', 'Upper Crust', 'The Good Breakfast',
                'Chozen Noodle', 'Coco Di Mama', 'Fresh Food Cafe', 'Costa Drive Thru'
            ]
            
            retail_shops = [
                'WHSmith', 'Marks & Spencer', 'Waitrose & Partners', 'Boots', 'Tesco Express', 'Spar'
            ]
            
            for brand in found_brands:
                if brand in food_outlets:
                    facilities['food_outlets'].append(brand)
                elif brand in retail_shops:
                    facilities['retail_shops'].append(brand)
            
            # Remove duplicates and sort
            facilities['food_outlets'] = sorted(list(set(facilities['food_outlets'])))
            facilities['retail_shops'] = sorted(list(set(facilities['retail_shops'])))
            
            # Detect amenities based on content
            amenity_keywords = {
                # Basic facilities
                'wifi': 'WiFi',
                'wi-fi': 'WiFi',
                'wireless': 'WiFi',
                'toilet': 'Toilets',
                'restroom': 'Toilets',
                'wc': 'Toilets',
                'parking': 'Parking',
                'car park': 'Parking',
                'fuel': 'Fuel Station',
                'petrol': 'Fuel Station',
                'diesel': 'Fuel Station',
                'baby chang': 'Baby Changing',
                'changing room': 'Baby Changing',
                'disabled access': 'Disabled Access',
                'wheelchair': 'Disabled Access',
                'accessible': 'Disabled Access',
                
                # Additional amenities
                'ev charging': 'EV Charging',
                'electric charging': 'EV Charging',
                'electric vehicle': 'EV Charging',
                'charging point': 'EV Charging',
                'travelodge': 'Travelodge',
                'hotel': 'Hotel',
                'accommodation': 'Hotel',
                'shower': 'Showers',
                'cash machine': 'Cash Machine',
                'atm': 'Cash Machine',
                'days inn': 'Days Inn'
            }
            
            for keyword, amenity in amenity_keywords.items():
                if keyword in all_text and amenity not in facilities['amenities']:
                    facilities['amenities'].append(amenity)
            
            facilities['amenities'] = sorted(list(set(facilities['amenities'])))
            
            return facilities
            
        except Exception as e:
            print(f"    Error scraping {url}: {str(e)}")
            return None

    def scrape_all_stations(self):
        """Scrape all stations from the master file"""
        try:
            print("🚗 Master Stations Scraper v1.0")
            print("=" * 50)
            print(f"📊 Scraping {len(self.master_stations)} stations")
            print()
            
            enhanced_stations = []
            urls_scraped = 0
            successful_scrapes = 0
            
            for i, station in enumerate(self.master_stations, 1):
                station_name = station['name']
                operator = station['operator']
                website_url = station.get('website_url')
                
                print(f"[{i:3d}/102] {station_name} ({operator})")
                
                if website_url:
                    print(f"  🔗 URL: {website_url}")
                    urls_scraped += 1
                    
                    # Scrape facilities
                    facilities = self.scrape_facilities_enhanced(website_url, operator)
                    
                    if facilities and any(facilities.values()):
                        print(f"  ✅ Scraped facilities successfully")
                        successful_scrapes += 1
                        
                        # Check for key brands
                        all_brands = facilities['food_outlets'] + facilities['retail_shops']
                        target_brands = ['Greggs', 'Marks & Spencer', 'Krispy Kreme', 'Costa Coffee', "McDonald's"]
                        found_targets = [brand for brand in target_brands if brand in all_brands]
                        if found_targets:
                            print(f"  🎯 Found: {', '.join(found_targets)}")
                    else:
                        print(f"  ⚠️  Scraping failed, no facilities data available")
                        facilities = {
                            'food_outlets': [],
                            'retail_shops': [],
                            'amenities': [],
                            'services': []
                        }
                else:
                    print(f"  ❌ No URL available, no facilities data")
                    facilities = {
                        'food_outlets': [],
                        'retail_shops': [],
                        'amenities': [],
                        'services': []
                    }
                
                # Build station object
                enhanced_station = {
                    'name': station_name,
                    'motorway': station['motorway'],
                    'location': station['location'],
                    'postcode': station['postcode'],
                    'coordinates': station['coordinates'],
                    'type': station['type'],
                    'operator': operator,
                    'parking_charges': station['parking_charges'],
                    'has_charge': station.get('has_charge'),
                    'is_single': station.get('is_single'),
                    'is_twin': station.get('is_twin'),
                    'has_walk': station.get('has_walk'),
                    'pair_name': station.get('pair_name'),
                    'is_pair': station.get('is_pair'),
                    'website_url': website_url,
                    'facilities': facilities
                }
                
                enhanced_stations.append(enhanced_station)
                
                # Respectful delay
                time.sleep(1)
            
            # Create output with metadata
            output = {
                'metadata': {
                    'last_updated': datetime.now().isoformat(),
                    'total_stations': len(enhanced_stations),
                    'successful_urls': urls_scraped,
                    'successful_scrapes': successful_scrapes,
                    'url_success_rate': f"{urls_scraped/len(enhanced_stations)*100:.1f}%",
                    'scrape_success_rate': f"{successful_scrapes/urls_scraped*100:.1f}%" if urls_scraped > 0 else "0%",
                    'data_source': 'Master Stations File + Real Website Scraping',
                    'scraper_version': 'Master Stations Scraper v1.0',
                    'operators_supported': list(set(s['operator'] for s in enhanced_stations)),
                    'scraping_features': [
                        'Master stations file as source',
                        'Direct URL scraping (no discovery needed)',
                        'Enhanced brand detection',
                        'Comprehensive facility mapping',
                        'Efficient processing'
                    ]
                },
                'service_stations': enhanced_stations
            }
            
            # Save to data directory
            output_file = '../data/uk_service_stations.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            print()
            print("=" * 50)
            print("🎉 Master Stations Scraping Complete!")
            print(f"📁 Saved to: {output_file}")
            print()
            print(f"📊 Final Statistics:")
            print(f"   Total stations: {len(enhanced_stations)}")
            print(f"   URLs available: {urls_scraped}/{len(enhanced_stations)} ({urls_scraped/len(enhanced_stations)*100:.1f}%)")
            print(f"   Successful scrapes: {successful_scrapes}/{urls_scraped} ({successful_scrapes/urls_scraped*100:.1f}%)" if urls_scraped > 0 else "   Successful scrapes: 0/0 (0%)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

def main():
    """Main execution function"""
    scraper = MasterStationsScraper()
    success = scraper.scrape_all_stations()
    
    if success:
        print()
        print("✅ Master Stations Scraping Complete!")
        print("🗂️ Updated data saved to ../data/uk_service_stations.json")
        print("🌐 Data ready for web interface!")
    else:
        print("❌ Scraping failed!")

if __name__ == "__main__":
    main()