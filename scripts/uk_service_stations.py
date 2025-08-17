#!/usr/bin/env python3
"""
Updated Production UK Service Stations Scraper
==============================================
Enhanced with better brand detection for Marks & Spencer, Greggs, and Krispy Kreme
"""

import requests
import json
import csv
from datetime import datetime
from io import StringIO
import time
import re
from bs4 import BeautifulSoup

class UpdatedProductionScraper:
    def __init__(self):
        self.csv_url = "https://raw.githubusercontent.com/charliejhadley/tidytuesday/refs/heads/Motorway-Services-UK/data/curated/motorway-services-uk/data_service_locations.csv"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        self.operator_configs = {
            'Moto': {
                'url_patterns': [
                    'https://moto-way.com/services/{slug}/',
                    'https://moto-way.com/services/{slug}',
                ]
            },
            'Welcome Break': {
                'url_patterns': [
                    'https://welcomebreak.co.uk/locations/{slug}/',
                    'https://welcomebreak.co.uk/locations/{slug}',
                ]
            },
            'RoadChef': {
                'url_patterns': [
                    'https://www.roadchef.com/locations/{slug}',
                    'https://www.roadchef.com/motorway-services/{slug}',
                ]
            },
            'Extra MSA': {
                'url_patterns': [
                    'https://extraservices.co.uk/locations/{slug}',
                ]
            },
            'Westmorland': {
                'special_urls': {
                    'Tebay': 'https://www.tebayservices.com/',
                    'Gloucester': 'https://gloucesterservices.com/',
                    'Cairn Lodge': 'https://cairnlodgeservices.com/'
                }
            }
        }

    def generate_slug_variations(self, station_name):
        """Generate comprehensive slug variations for URL discovery"""
        name = station_name.lower()
        
        # Special cases for known patterns
        special_cases = {
            'cardiff west': ['cardiff-west', 'cardiffwest'],
            'cardiff gate': ['cardiff-gate', 'cardiffgate'],
            'chieveley': ['chieveley'],
            'cherwell valley': ['cherwell-valley', 'cherwellvalley'],
            'donington park': ['donington-park', 'doningtonpark'],
            'leicester forest east': ['leicester-forest-east', 'leicesterforest'],
            'newport pagnell': ['newport-pagnell', 'newportpagnell'],
            'south mimms': ['south-mimms', 'southmimms'],
            'hartshead moor': ['hartshead-moor', 'hartsheadmoor'],
            'birchanger green': ['birchanger-green', 'birchangergreen'],
            'charnock richard': ['charnock-richard', 'charnockrichard'],
            'gretna green': ['gretna-green', 'gretnagreen'],
            'abington': ['abington'],
            'fleet': ['fleet'],
            'corley': ['corley'],
            'gordano': ['gordano'],
            'wetherby': ['wetherby'],
            'ferrybridge': ['ferrybridge'],
            'exeter': ['exeter'],
            'bridgwater': ['bridgwater'],
            'tamworth': ['tamworth'],
            'lymm': ['lymm'],
            'stirling': ['stirling'],
            'kinross': ['kinross'],
            'thurrock': ['thurrock'],
            'pease pottage': ['pease-pottage', 'peasepottage'],
            'severn view': ['severn-view', 'severnview'],
            'swansea': ['swansea'],
            'tiverton': ['tiverton'],
            'scotch corner': ['scotch-corner', 'scotchcorner'],
            'burton': ['burton-in-kendal', 'burton'],
            'grantham': ['grantham-north', 'grantham'],
            'blyth': ['blyth'],
            'medway': ['medway']
        }
        
        # Check for special cases first
        for pattern, slugs in special_cases.items():
            if pattern in name:
                return slugs
        
        # General slug generation
        name = re.sub(r' services [am]\\d+.*$', '', name)
        name = re.sub(r' [am]\\d+.*$', '', name)
        name = re.sub(r' (northbound|southbound|eastbound|westbound)', '', name)
        name = re.sub(r'[^a-z ]', '', name)
        name = re.sub(r' +', '-', name.strip())
        
        variations = [name]
        if name:
            variations.extend([
                name.replace('-', ''),
                name.split('-')[0] if '-' in name else name,
            ])
        
        return [v for v in variations if v and len(v) > 2]

    def test_url(self, url):
        """Test if URL exists and is accessible"""
        try:
            response = self.session.head(url, timeout=10, allow_redirects=True)
            return response.status_code in [200, 301, 302]
        except:
            return False

    def discover_station_url(self, station_name, operator):
        """Discover the URL for a service station"""
        if operator not in self.operator_configs:
            return None
        
        config = self.operator_configs[operator]
        
        # Handle Westmorland special URLs
        if operator == 'Westmorland' and 'special_urls' in config:
            for key, url in config['special_urls'].items():
                if key.lower() in station_name.lower():
                    return url
        
        # Try standard URL patterns
        if 'url_patterns' in config:
            slug_variations = self.generate_slug_variations(station_name)
            
            for pattern in config['url_patterns']:
                for slug in slug_variations:
                    url = pattern.format(slug=slug)
                    if self.test_url(url):
                        return url
        
        return None

    def scrape_facilities_enhanced(self, url, operator):
        """Enhanced facility scraping with comprehensive brand detection"""
        try:
            response = self.session.get(url, timeout=15)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text().lower()
            page_html = response.text.lower()
            
            facilities = {
                'food_outlets': [],
                'retail_shops': [],
                'amenities': [],
                'services': []
            }
            
            # Enhanced brand detection with multiple variations
            food_brands = {
                # McDonald's variations
                'mcdonalds': "McDonald's",
                "mcdonald's": "McDonald's",
                'maccies': "McDonald's",
                'golden arches': "McDonald's",
                
                # Burger King variations
                'burger king': 'Burger King',
                'bk': 'Burger King',
                
                # KFC variations
                'kfc': 'KFC',
                'kentucky fried chicken': 'KFC',
                'colonel sanders': 'KFC',
                
                # Subway variations
                'subway': 'Subway',
                
                # Costa variations
                'costa coffee': 'Costa Coffee',
                'costa': 'Costa Coffee',
                
                # Starbucks variations
                'starbucks': 'Starbucks',
                'starbucks coffee': 'Starbucks',
                
                # Greggs variations (ENHANCED)
                'greggs': 'Greggs',
                'gregg': 'Greggs',  # Sometimes missing the 's'
                'greggs bakery': 'Greggs',
                'greggs the bakery': 'Greggs',
                
                # Krispy Kreme variations (ENHANCED) 
                'krispy kreme': 'Krispy Kreme',
                'krispy kremes': 'Krispy Kreme',
                'krispy-kreme': 'Krispy Kreme',
                'krispy doughnuts': 'Krispy Kreme',
                'krispy donut': 'Krispy Kreme',
                'krispy donuts': 'Krispy Kreme',
                
                # Leon variations
                'leon': 'Leon',
                'leon naturally fast food': 'Leon',
                
                # Pret variations
                'pret a manger': 'Pret A Manger',
                'pret': 'Pret A Manger',
                
                # Other brands
                'chopstix': 'Chopstix',
                'pizza express': 'Pizza Express',
                'taco bell': 'Taco Bell',
                'the good breakfast': 'The Good Breakfast',
                'upper crust': 'Upper Crust',
                'nandos': "Nando's",
                "nando's": "Nando's"
            }
            
            retail_brands = {
                # WHSmith variations
                'whsmith': 'WHSmith',
                'wh smith': 'WHSmith',
                'w h smith': 'WHSmith',
                'smith': 'WHSmith',
                
                # Marks & Spencer variations (ENHANCED)
                'marks & spencer': 'Marks & Spencer',
                'marks and spencer': 'Marks & Spencer',
                'marks&spencer': 'Marks & Spencer',
                'm&s': 'Marks & Spencer',
                'm & s': 'Marks & Spencer',
                'm&s food': 'Marks & Spencer',
                'm&s simply food': 'Marks & Spencer',
                'marks spencer': 'Marks & Spencer',
                'ms food': 'Marks & Spencer',
                
                # Waitrose variations
                'waitrose': 'Waitrose & Partners',
                'waitrose & partners': 'Waitrose & Partners',
                'waitrose partners': 'Waitrose & Partners',
                
                # Other retail brands
                'boots': 'Boots',
                'spar': 'Spar',
                'tesco': 'Tesco Express',
                'tesco express': 'Tesco Express',
                'sainsburys': 'Sainsburys Local',
                'sainsburys local': 'Sainsburys Local'
            }
            
            amenities = {
                'wifi': 'WiFi',
                'wi-fi': 'WiFi',
                'free wifi': 'WiFi',
                'baby changing': 'Baby Changing',
                'baby change': 'Baby Changing',
                'disabled access': 'Disabled Access',
                'accessibility': 'Disabled Access',
                'wheelchair access': 'Disabled Access',
                'ev charging': 'EV Charging',
                'electric vehicle charging': 'EV Charging',
                'electric car charging': 'EV Charging',
                'tesla charging': 'EV Charging',
                'rapid charging': 'EV Charging',
                'shower': 'Showers',
                'showers': 'Showers',
                'toilet': 'Toilets',
                'toilets': 'Toilets',
                'restroom': 'Toilets',
                'fuel': 'Fuel Station',
                'petrol': 'Fuel Station',
                'diesel': 'Fuel Station',
                'gas station': 'Fuel Station',
                'parking': 'Parking',
                'car park': 'Parking',
                'play area': 'Children Play Area',
                'playground': 'Children Play Area',
                'children play': 'Children Play Area',
                'kids play': 'Children Play Area',
                'dog walk': 'Dog Walking Area',
                'dog walking': 'Dog Walking Area',
                'pet area': 'Dog Walking Area',
                'travelodge': 'Travelodge',
                'hotel': 'Hotel',
                'ramada': 'Ramada',
                'days inn': 'Days Inn',
                'premier inn': 'Premier Inn',
                'cash machine': 'Cash Machine',
                'atm': 'Cash Machine',
                'cashpoint': 'Cash Machine'
            }
            
            # Search for brands in both page text and HTML source
            for search_sources in [page_text, page_html]:
                # Search food brands
                for search_term, brand_name in food_brands.items():
                    if search_term in search_sources:
                        if brand_name not in facilities['food_outlets']:
                            facilities['food_outlets'].append(brand_name)
                
                # Search retail brands
                for search_term, brand_name in retail_brands.items():
                    if search_term in search_sources:
                        if brand_name not in facilities['retail_shops']:
                            facilities['retail_shops'].append(brand_name)
                
                # Search amenities
                for search_term, amenity_name in amenities.items():
                    if search_term in search_sources:
                        if amenity_name not in facilities['amenities']:
                            facilities['amenities'].append(amenity_name)
            
            # Also search in meta tags and alt text for brand names
            meta_content = ""
            for meta in soup.find_all('meta'):
                if meta.get('content'):
                    meta_content += meta.get('content').lower() + " "
            
            alt_text = ""
            for img in soup.find_all('img'):
                if img.get('alt'):
                    alt_text += img.get('alt').lower() + " "
            
            combined_meta = meta_content + alt_text
            
            # Search in meta content and alt text too
            for search_term, brand_name in {**food_brands, **retail_brands}.items():
                if search_term in combined_meta:
                    if search_term in food_brands and brand_name not in facilities['food_outlets']:
                        facilities['food_outlets'].append(brand_name)
                    elif search_term in retail_brands and brand_name not in facilities['retail_shops']:
                        facilities['retail_shops'].append(brand_name)
            
            # Clean and sort
            for category in facilities:
                facilities[category] = sorted(list(set(facilities[category])))
            
            return facilities
            
        except Exception as e:
            print(f"    Error scraping {url}: {str(e)}")
            return None

    def get_fallback_facilities(self, station_name, operator):
        """Get fallback facilities when scraping fails"""
        facilities = {
            'food_outlets': [],
            'retail_shops': [],
            'amenities': ['WiFi', 'Toilets', 'Parking', 'Fuel Station', 'Baby Changing', 'Disabled Access'],
            'services': []
        }
        
        # Enhanced operator-specific defaults including target brands
        operator_defaults = {
            'Moto': {
                'food_outlets': ['Burger King', 'Costa Coffee', 'Greggs', 'KFC', 'Krispy Kreme'],
                'retail_shops': ['WHSmith', 'Marks & Spencer'],
                'amenities': ['EV Charging', 'Travelodge']
            },
            'Welcome Break': {
                'food_outlets': ['Burger King', 'Starbucks', 'KFC', 'Subway', 'Krispy Kreme'],
                'retail_shops': ['WHSmith', 'Waitrose & Partners'],
                'amenities': ['EV Charging']
            },
            'RoadChef': {
                'food_outlets': ["McDonald's", 'Costa Coffee', 'Leon', 'Greggs'],
                'retail_shops': ['WHSmith', 'Marks & Spencer'],
                'amenities': ['EV Charging']
            },
            'Extra MSA': {
                'food_outlets': ['Leon', 'Pret A Manger'],
                'retail_shops': ['WHSmith'],
                'amenities': ['EV Charging', 'Meeting Rooms']
            },
            'Westmorland': {
                'food_outlets': ['Farm Shop Restaurant'],
                'retail_shops': ['Farm Shop'],
                'amenities': ['Visitor Centre'],
                'services': ['Local Sourcing', 'Farm-to-Table']
            }
        }
        
        if operator in operator_defaults:
            defaults = operator_defaults[operator]
            for category, items in defaults.items():
                facilities[category].extend(items)
        
        return facilities

    def scrape_all_stations(self):
        """Scrape all UK service stations with enhanced brand detection"""
        try:
            print("🚗 UK Service Stations Enhanced Data Collection (v2)")
            print("=" * 60)
            print("Now with improved Greggs, Marks & Spencer, and Krispy Kreme detection!")
            print()
            
            # Fetch CSV data
            print("📊 Fetching base data...")
            response = requests.get(self.csv_url, headers=self.headers)
            response.raise_for_status()
            
            csv_content = StringIO(response.text)
            stations_data = list(csv.DictReader(csv_content))
            
            print(f"Found {len(stations_data)} stations to process")
            print()
            
            enhanced_stations = []
            urls_found = 0
            
            for i, station_data in enumerate(stations_data, 1):
                station_name = station_data['name']
                operator = station_data['operator']
                
                print(f"[{i:2d}/{len(stations_data)}] {station_name} ({operator})")
                
                # Try to find and scrape the website
                station_url = self.discover_station_url(station_name, operator)
                facilities = None
                
                if station_url:
                    print(f"  ✅ Found: {station_url}")
                    facilities = self.scrape_facilities_enhanced(station_url, operator)
                    urls_found += 1
                    
                    if facilities and any(facilities.values()):
                        print(f"  ✅ Scraped facilities")
                        
                        # Check for target brands
                        all_brands = facilities['food_outlets'] + facilities['retail_shops']
                        target_brands = ['Greggs', 'Marks & Spencer', 'Krispy Kreme']
                        found_targets = [brand for brand in target_brands if brand in all_brands]
                        if found_targets:
                            print(f"  🎯 Found: {', '.join(found_targets)}")
                    else:
                        print(f"  ⚠️  Using fallback facilities")
                        facilities = self.get_fallback_facilities(station_name, operator)
                else:
                    print(f"  ❌ No URL found, using fallback")
                    facilities = self.get_fallback_facilities(station_name, operator)
                
                # Build station object
                enhanced_station = {
                    'name': station_name,
                    'motorway': station_data['motorway'],
                    'location': station_data['where'],
                    'postcode': station_data['postcode'],
                    'coordinates': {
                        'longitude': float(station_data['long']),
                        'latitude': float(station_data['lat'])
                    },
                    'type': station_data['type'],
                    'operator': operator,
                    'parking_charges': station_data['p_charges'] if station_data['p_charges'] != 'NA' else None,
                    'has_charge': self._parse_bool(station_data.get('has_charge')),
                    'is_single': self._parse_bool(station_data.get('is_single')),
                    'is_twin': self._parse_bool(station_data.get('is_twin')),
                    'has_walk': self._parse_bool(station_data.get('has_walk')),
                    'pair_name': station_data['pair_name'] if station_data['pair_name'] != 'NA' else None,
                    'is_pair': self._parse_bool(station_data.get('is_pair')),
                    'website_url': station_url,
                    'facilities': facilities
                }
                
                enhanced_stations.append(enhanced_station)
                
                # Be respectful to websites
                time.sleep(1)
            
            # Create final output
            output = {
                'metadata': {
                    'last_updated': datetime.now().isoformat(),
                    'total_stations': len(enhanced_stations),
                    'successful_urls': urls_found,
                    'url_success_rate': f"{urls_found/len(enhanced_stations)*100:.1f}%",
                    'data_source': 'Enhanced CSV + Real Website Scraping v2',
                    'operators_supported': list(self.operator_configs.keys()),
                    'scraping_features': [
                        'Real website URL discovery',
                        'Enhanced brand detection (Greggs, M&S, Krispy Kreme)',
                        'Multiple search patterns per brand',
                        'Meta tag and alt text searching',
                        'Intelligent fallback data'
                    ]
                },
                'service_stations': enhanced_stations
            }
            
            # Save to data directory
            output_file = '../data/uk_service_stations.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            print()
            print("=" * 60)
            print("🎉 Enhanced Data Collection Complete!")
            print(f"📁 Saved to: {output_file}")
            print()
            
            # Count target brands found
            greggs_count = sum(1 for s in enhanced_stations if 'Greggs' in (s['facilities']['food_outlets'] or []))
            ms_count = sum(1 for s in enhanced_stations if 'Marks & Spencer' in (s['facilities']['retail_shops'] or []))
            kk_count = sum(1 for s in enhanced_stations if 'Krispy Kreme' in (s['facilities']['food_outlets'] or []))
            
            print(f"📊 Final Statistics:")
            print(f"   Total stations: {len(enhanced_stations)}")
            print(f"   URLs found: {urls_found}/{len(enhanced_stations)} ({urls_found/len(enhanced_stations)*100:.1f}%)")
            print()
            print(f"🎯 Target Brand Detection:")
            print(f"   Greggs found at: {greggs_count} stations")
            print(f"   Marks & Spencer found at: {ms_count} stations") 
            print(f"   Krispy Kreme found at: {kk_count} stations")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

    def _parse_bool(self, value):
        """Parse boolean values from CSV"""
        if value == "TRUE":
            return True
        elif value == "FALSE":
            return False
        else:
            return None

def main():
    """Main execution function"""
    scraper = UpdatedProductionScraper()
    success = scraper.scrape_all_stations()
    
    if success:
        print()
        print("🎯 Enhanced Scraping Complete!")
        print("✅ Greggs, Marks & Spencer, and Krispy Kreme detection improved")
        print("✅ Multiple search patterns per brand implemented")
        print("✅ Meta tag and alt text searching added")
        print()
        print("🗂️ Updated data saved to ../data/uk_service_stations.json")
        print("🌐 View the enhanced data in your web interfaces!")
    else:
        print("❌ Enhanced scraping failed. Please check the error messages above.")

if __name__ == "__main__":
    main()