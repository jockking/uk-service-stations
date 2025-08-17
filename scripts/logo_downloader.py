#!/usr/bin/env python3
"""
Brand Logo Downloader
====================
Downloads all food brand logos as PNG files and stores them locally
"""

import requests
import os
from urllib.parse import urlparse
import time

class LogoDownloader:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.images_dir = '../web/images'
        
        # Ensure images directory exists
        os.makedirs(self.images_dir, exist_ok=True)

    def download_logo(self, brand_name, logo_url, filename):
        """Download a single logo"""
        try:
            print(f"  📥 Downloading {brand_name}...")
            
            response = requests.get(logo_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # Save the file
            filepath = os.path.join(self.images_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"  ✅ Saved {filename}")
            return True
            
        except Exception as e:
            print(f"  ❌ Failed to download {brand_name}: {str(e)}")
            return False

    def download_all_logos(self):
        """Download all food brand logos"""
        
        # High-quality logo URLs (PNG preferred) - Updated with working sources
        brand_logos = {
            "mcdonalds": {
                "url": "https://logos-world.net/wp-content/uploads/2020/04/McDonalds-Logo.png",
                "filename": "mcdonalds.png"
            },
            "burger-king": {
                "url": "https://logos-world.net/wp-content/uploads/2020/04/Burger-King-Logo.png", 
                "filename": "burger-king.png"
            },
            "kfc": {
                "url": "https://logos-world.net/wp-content/uploads/2020/04/KFC-Logo.png",
                "filename": "kfc.png"
            },
            "subway": {
                "url": "https://cdn.worldvectorlogo.com/logos/subway-2.svg",
                "filename": "subway.png"
            },
            "costa-coffee": {
                "url": "https://cdn.worldvectorlogo.com/logos/costa-coffee.svg",
                "filename": "costa-coffee.png"
            },
            "starbucks": {
                "url": "https://cdn.worldvectorlogo.com/logos/starbucks-coffee-company.svg",
                "filename": "starbucks.png"
            },
            "greggs": {
                "url": "https://vectorseek.com/wp-content/uploads/2023/09/Greggs-Logo-Vector.svg-.png",
                "filename": "greggs.png"
            },
            "krispy-kreme": {
                "url": "https://cdn.worldvectorlogo.com/logos/krispy-kreme.svg",
                "filename": "krispy-kreme.png"
            },
            "leon": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Leon_logo.svg/1200px-Leon_logo.svg.png",
                "filename": "leon.png"
            },
            "pret-a-manger": {
                "url": "https://cdn.worldvectorlogo.com/logos/pret-a-manger.svg",
                "filename": "pret-a-manger.png"
            },
            "pizza-express": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/PizzaExpress_logo.svg/1200px-PizzaExpress_logo.svg.png",
                "filename": "pizza-express.png"
            },
            "nandos": {
                "url": "https://cdn.worldvectorlogo.com/logos/nandos.svg",
                "filename": "nandos.png"
            },
            "taco-bell": {
                "url": "https://cdn.worldvectorlogo.com/logos/taco-bell-1.svg",
                "filename": "taco-bell.png"
            },
            "upper-crust": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Upper_Crust_logo.svg/1200px-Upper_Crust_logo.svg.png",
                "filename": "upper-crust.png"
            },
            # Retail brands
            "whsmith": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/WHSmith_logo.svg/1200px-WHSmith_logo.svg.png",
                "filename": "whsmith.png"
            },
            "marks-and-spencer": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Marks_%26_Spencer_logo.svg/1200px-Marks_%26_Spencer_logo.svg.png",
                "filename": "marks-and-spencer.png"
            },
            "waitrose": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Waitrose_%26_Partners_logo.svg/1200px-Waitrose_%26_Partners_logo.svg.png",
                "filename": "waitrose.png"
            },
            "boots": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Boots_logo.svg/1200px-Boots_logo.svg.png",
                "filename": "boots.png"
            },
            "tesco": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Tesco_Logo.svg/1200px-Tesco_Logo.svg.png",
                "filename": "tesco.png"
            }
        }
        
        print("🎨 Downloading Brand Logos")
        print("=" * 40)
        
        successful_downloads = 0
        total_logos = len(brand_logos)
        
        for brand_key, logo_info in brand_logos.items():
            success = self.download_logo(
                brand_key.replace('-', ' ').title(),
                logo_info['url'],
                logo_info['filename']
            )
            
            if success:
                successful_downloads += 1
            
            # Be respectful to the server
            time.sleep(1)
        
        print()
        print("=" * 40)
        print(f"🎉 Logo Download Complete!")
        print(f"✅ Successfully downloaded: {successful_downloads}/{total_logos} logos")
        print(f"📁 Saved to: {self.images_dir}")
        
        # List downloaded files
        print()
        print("📋 Downloaded Files:")
        try:
            files = sorted(os.listdir(self.images_dir))
            for file in files:
                if file.endswith('.png'):
                    filepath = os.path.join(self.images_dir, file)
                    size = os.path.getsize(filepath)
                    print(f"   • {file} ({size:,} bytes)")
        except Exception as e:
            print(f"   Error listing files: {str(e)}")
        
        return successful_downloads == total_logos

def main():
    downloader = LogoDownloader()
    downloader.download_all_logos()

if __name__ == "__main__":
    main()