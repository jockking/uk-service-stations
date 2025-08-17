# UK Service Stations Explorer

A comprehensive web scraping and visualization project for UK motorway service stations data, featuring real-time data collection from operator websites and an interactive web interface.

## 📁 Project Structure

```
uk-service-stations/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── data/                  # Data files
│   ├── uk_service_stations.json    # Main dataset (scraped data)
│   ├── master_service_stations.json # Master stations file with URLs
│   └── stations_missing_urls.json  # Reference for missing URLs
├── scripts/               # Python scripts
│   ├── uk_service_stations.py      # Master stations scraper (uses master file)
│   ├── logo_downloader.py           # Downloads brand logos
│   └── create_placeholder_logos.py # Creates placeholder logos
├── web/                   # Web interface
│   ├── index.html         # Interactive web frontend with logos & map
│   ├── map_view.html      # Map-focused view
│   └── images/            # Brand logo images
├── docs/                  # Documentation
│   └── CLAUDE.md          # Claude Code guidance
└── tests/                 # Test files (empty - ready for future tests)
```

## 🚀 Features

### Data Collection
- **Master File Based**: Uses comprehensive master stations file with 99% URL coverage
- **Real Website Scraping**: Collects actual facilities data from operator websites
- **Multiple Operators**: Supports Moto, Welcome Break, RoadChef, Extra MSA, Westmorland + more
- **Comprehensive Data**: Name, location, coordinates, facilities, amenities, parking charges
- **Efficient Processing**: Direct URL scraping without discovery overhead

### Web Interface
- **Interactive Dashboard**: Modern, responsive design
- **Advanced Filtering**: Search by name, operator, motorway, facilities
- **Detailed Views**: Click stations for complete information
- **Real-time Updates**: Live filtering and statistics
- **Mobile Responsive**: Works on all devices

## 📊 Current Dataset

- **45 Service Stations** (partial dataset from recent scraping)
- **Real Facilities Data** scraped from operator websites
- **Accurate Information** including food outlets, retail shops, amenities
- **Website Links** to official station pages

## 🛠 Installation & Usage

### Prerequisites
```bash
pip install requests beautifulsoup4
```

### Running the Scraper
```bash
# Navigate to scripts directory
cd scripts

# Run the enhanced scraper (scrapes real website data)
python uk_service_stations.py

# Test single station (Cardiff West example)
python test_single_station.py
```

### Viewing the Web Interface
1. Open `web/index.html` in any modern web browser
2. The interface will automatically load data from `data/uk_service_stations.json`
3. Use filters and search to explore the service stations

### Running from Project Root
```bash
# Start a simple HTTP server to avoid CORS issues
python -m http.server 8000

# Then visit: http://localhost:8000/web/
```

## 📋 Data Structure

Each service station includes:
- **Basic Info**: Name, motorway, location, postcode, coordinates
- **Operator Details**: Company, parking charges, site configuration
- **Facilities**: Food outlets, retail shops, amenities categorized
- **Website URL**: Direct link to official station page

Example structure:
```json
{
  "name": "Cardiff West Services M4",
  "motorway": "M4",
  "operator": "Moto",
  "website_url": "https://moto-way.com/services/cardiff-west/",
  "facilities": {
    "food_outlets": ["Costa Coffee", "Burger King", "KFC", "Greggs"],
    "retail_shops": ["WHSmith"],
    "amenities": ["WiFi", "EV Charging", "Travelodge", "Baby Changing"]
  }
}
```

## 🔧 Configuration

### Operator URLs (in uk_service_stations.py)
The scraper includes URL patterns for major operators:
- **Moto**: `https://moto-way.com/services/{slug}/`
- **Welcome Break**: `https://welcomebreak.co.uk/locations/{slug}/`
- **RoadChef**: `https://www.roadchef.com/locations/{slug}`

### Scraping Delays
- 2-second delays between requests for respectful scraping
- Timeout settings for network requests
- Error handling with fallback to database

## 📈 Performance

- **URL Discovery**: Automatically finds correct station URLs
- **Facilities Extraction**: Parses HTML to identify actual brands and amenities
- **Data Validation**: Cleans and categorizes facility information
- **Fallback System**: Uses operator database if scraping fails

## 🎯 Future Enhancements

- **Complete Dataset**: Scrape all 102+ UK service stations
- **Regular Updates**: Scheduled scraping for data freshness
- **Map Integration**: Add geographical visualization
- **Mobile App**: Native mobile interface
- **API Endpoint**: REST API for data access

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is for educational and research purposes. Please respect the terms of service of the websites being scraped.

## 🙏 Acknowledgments

- Data source: GitHub CSV from charliejhadley/tidytuesday
- Operator websites: Moto, Welcome Break, RoadChef, Extra MSA, Westmorland
- Icons: Font Awesome
- Design inspiration: Modern web design principles