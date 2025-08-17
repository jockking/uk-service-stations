# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive UK service stations data collection and visualization project. It includes Python web scraping scripts that collect real facility data from operator websites, and a modern web interface for exploring the data.

## Project Structure

```
├── scripts/               # Python scraping scripts
├── data/                  # JSON data files
├── web/                   # Web interface files
├── docs/                  # Documentation
├── tests/                 # Test files
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
```

## Key Files

### Scripts Directory
- `scripts/uk_service_stations.py` - Main production scraper with real website scraping
- `scripts/logo_downloader.py` - Downloads brand logos for web interface
- `scripts/create_placeholder_logos.py` - Creates placeholder logo images

### Data Directory
- `data/uk_service_stations.json` - Main dataset with scraped facilities
- `data/test_cardiff_west.json` - Sample test data

### Web Directory
- `web/index.html` - Interactive web frontend with brand logos and map view
- `web/map_view.html` - Dedicated map view interface
- `web/images/` - Brand logo images for food outlets and retail shops

## Dependencies

Install from requirements.txt:
```bash
pip install -r requirements.txt
```

Or manually install:
```bash
pip install requests beautifulsoup4
```

## Running the Project

### Data Collection
```bash
cd scripts
python uk_service_stations.py
```

### Web Interface
```bash
# Option 1: Open directly
open web/index.html

# Option 2: Use HTTP server (recommended)
python -m http.server 8000
# Then visit: http://localhost:8000/web/
```

## Architecture Notes

- `ServiceStationScraper` class handles all scraping logic
- Implements respectful scraping with 1-second delays between requests
- Uses proper User-Agent headers to avoid blocking
- Includes error handling and progress reporting
- Outputs structured JSON with metadata (timestamp, total count)

## Code Structure

The improved scraper (`uk_service_stations.py`) follows this flow:
1. `_get_motorway_list()` - Discovers all motorway pages
2. `_scrape_motorway_stations()` - Finds stations for each motorway
3. `_scrape_station_page()` - Extracts detailed station information
4. Data is aggregated and saved to JSON with metadata

## Data Output

The JSON output includes:
- `last_updated` - ISO timestamp of scraping
- `total_stations` - Count of scraped stations
- `data_source` - Source attribution for the data
- `service_stations` - Array of detailed station objects

### Station Object Structure

Each station includes:
- Basic info: name, motorway, location, postcode, coordinates
- Operator details: operator, parking charges, site configuration
- Enhanced facilities data:
  - `mandatory_facilities` - Required amenities (toilets, parking, EV charging, etc.)
  - `food_outlets` - Restaurants and food chains (McDonalds, Costa, etc.)
  - `retail_shops` - Shops and services (WHSmith, M&S, etc.)
  - `amenities` - Additional features (WiFi, play areas, hotels, etc.)
  - `services` - Special services (local sourcing, visitor centres, etc.)

### Facilities Database

The scraper includes a comprehensive facilities database that maps:
- Operator-specific standard facilities and common brands
- Special facilities for notable locations (Gloucester, Tebay, etc.)
- Mandatory facilities required by UK law
- Food chains and retail outlets commonly found at service stations