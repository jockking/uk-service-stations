#!/usr/bin/env python3
"""
Look for API endpoints or data URLs in Watford Gap scripts
"""

import requests
import re
from bs4 import BeautifulSoup

def find_api_endpoints():
    url = "https://www.roadchef.com/motorway-services/watford-gap"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print("Looking for API endpoints in Watford Gap...")
    print("=" * 60)
    
    response = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Get all script content
    all_script_content = ""
    for script in soup.find_all('script'):
        if script.string:
            all_script_content += script.string + "\n"
    
    print(f"Total script content: {len(all_script_content)} characters")
    
    # Look for common API patterns
    api_patterns = [
        r'https?://[^"\s]+api[^"\s]*',  # API URLs
        r'https?://[^"\s]+\.json[^"\s]*',  # JSON endpoints
        r'/api/[^"\s]*',  # Relative API paths
        r'fetch\([^)]+\)',  # Fetch calls
        r'axios\.[^(]+\([^)]+\)',  # Axios calls
        r'\.get\([^)]+\)',  # GET requests
        r'endpoint["\s]*:["\s]*[^,"]+',  # Endpoint configurations
        r'baseURL["\s]*:["\s]*[^,"]+',  # Base URLs
    ]
    
    print("\nSearching for API patterns...")
    found_any = False
    
    for pattern_name, pattern in [
        ("API URLs", r'https?://[^"\s]+api[^"\s]*'),
        ("JSON endpoints", r'https?://[^"\s]+\.json[^"\s]*'),
        ("Relative API paths", r'/api/[^"\s]*'),
        ("Fetch calls", r'fetch\([^)]+\)'),
        ("Axios calls", r'axios\.[^(]+\([^)]+\)'),
        ("GET requests", r'\.get\([^)]+\)'),
        ("Endpoint configs", r'endpoint["\s]*:["\s]*[^,"]+'),
        ("Base URLs", r'baseURL["\s]*:["\s]*[^,"]+'),
    ]:
        matches = re.findall(pattern, all_script_content, re.IGNORECASE)
        if matches:
            print(f"\n{pattern_name}:")
            for match in matches[:5]:  # Show first 5 matches
                print(f"  {match}")
            if len(matches) > 5:
                print(f"  ... and {len(matches) - 5} more")
            found_any = True
    
    if not found_any:
        print("❌ No obvious API patterns found")
    
    # Look for any URLs that might contain data
    print("\nLooking for data-related URLs...")
    url_patterns = re.findall(r'https?://[^"\s]+', all_script_content)
    data_urls = [url for url in url_patterns if any(keyword in url.lower() 
                for keyword in ['data', 'content', 'info', 'details', 'watford'])]
    
    if data_urls:
        print("Potential data URLs:")
        for url in data_urls:
            print(f"  {url}")
    else:
        print("❌ No data-related URLs found")
    
    # Look for variable assignments that might contain data
    print("\nLooking for data variables...")
    var_patterns = [
        r'var\s+\w*[dD]ata\w*\s*=\s*[^;]+',
        r'const\s+\w*[dD]ata\w*\s*=\s*[^;]+',
        r'let\s+\w*[dD]ata\w*\s*=\s*[^;]+',
        r'\w*[bB]rands?\w*\s*[:=]\s*[^;,}]+',
        r'\w*[fF]acilities?\w*\s*[:=]\s*[^;,}]+',
    ]
    
    for pattern in var_patterns:
        matches = re.findall(pattern, all_script_content, re.IGNORECASE)
        if matches:
            print("Data variable assignments:")
            for match in matches[:3]:
                print(f"  {match[:100]}...")
            break

if __name__ == "__main__":
    find_api_endpoints()