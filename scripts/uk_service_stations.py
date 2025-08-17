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

    def scrape_facilities_enhanced(self, url, operator):
        """Enhanced facility scraping with comprehensive brand detection"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
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
                'amenities': ['WiFi', 'Toilets', 'Parking', 'Fuel Station', 'Baby Changing', 'Disabled Access'],
                'services': []
            }
            
            # Extract all text content
            page_text = soup.get_text().lower()
            
            # Enhanced brand detection
            found_brands = set()
            for search_term, brand_name in brand_mapping.items():
                if search_term in page_text:
                    found_brands.add(brand_name)
            
            # Also check in meta tags, alt texts, and specific elements
            for element in soup.find_all(['img', 'a', 'div', 'span'], alt=True):
                alt_text = element.get('alt', '').lower()
                for search_term, brand_name in brand_mapping.items():
                    if search_term in alt_text:
                        found_brands.add(brand_name)
            
            # Categorize brands
            food_outlets = [
                'Burger King', "McDonald's", 'KFC', 'Subway', 'Costa Coffee', 'Starbucks',
                'Greggs', 'Krispy Kreme', 'Pret A Manger', 'Leon', 'Pizza Express',
                "Nando's", 'Chopstix', 'Taco Bell', 'Upper Crust', 'The Good Breakfast'
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
            
            # Add common amenities based on content
            amenity_keywords = {
                'ev charging': 'EV Charging',
                'electric charging': 'EV Charging',
                'electric vehicle': 'EV Charging',
                'travelodge': 'Travelodge',
                'hotel': 'Hotel',
                'accommodation': 'Hotel',
                'shower': 'Showers',
                'cash machine': 'Cash Machine',
                'atm': 'Cash Machine',
                'days inn': 'Days Inn'
            }
            
            for keyword, amenity in amenity_keywords.items():
                if keyword in page_text and amenity not in facilities['amenities']:
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
                        print(f"  ⚠️  Scraping failed, using basic amenities")
                        facilities = {
                            'food_outlets': [],
                            'retail_shops': [],
                            'amenities': ['WiFi', 'Toilets', 'Parking', 'Fuel Station', 'Baby Changing', 'Disabled Access'],
                            'services': []
                        }
                else:
                    print(f"  ❌ No URL available")
                    facilities = {
                        'food_outlets': [],
                        'retail_shops': [],
                        'amenities': ['WiFi', 'Toilets', 'Parking', 'Fuel Station', 'Baby Changing', 'Disabled Access'],
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