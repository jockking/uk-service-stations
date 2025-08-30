# UK Service Stations Explorer

A comprehensive web scraping and visualization project for UK motorway service stations data, featuring real-time data collection from operator websites, an interactive web interface, and cross-platform mobile apps.

## 📁 Project Structure

```
uk-service-stations/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── data/                  # Data files
│   ├── uk_service_stations.json      # Main dataset (102 stations)
│   ├── master_service_stations.json  # Master stations file with URLs
│   └── stations_missing_urls.json    # Reference for missing URLs
├── scripts/               # Python scripts
│   ├── uk_service_stations.py        # Master stations scraper
│   ├── logo_downloader.py            # Downloads brand logos
│   ├── create_placeholder_logos.py   # Creates placeholder logos
│   └── test_precision_fix.py         # Brand detection testing
├── UKServiceStations/     # React Native mobile app
│   ├── src/components/    # Mobile UI components
│   ├── android/           # Android build configuration
│   ├── ios/               # iOS build configuration
│   └── MOBILE_APP_GUIDE.md # Mobile development guide
├── images/                # Brand logo images (29 operators)
├── index.html             # Interactive web frontend with map
├── map_view.html          # Map-focused view
├── docs/                  # Documentation
│   └── CLAUDE.md          # Claude Code guidance
└── tests/                 # Test files
```

## 🚀 Features

### Data Collection
- **Complete Coverage**: 102 UK motorway service stations with 100% URL coverage
- **Real Website Scraping**: Live data from operator websites with 99% success rate
- **8 Major Operators**: Moto, Welcome Break, RoadChef, Extra MSA, Westmorland, Euro Garages, Stop 24, BP Connect
- **Comprehensive Data**: Name, location, coordinates, facilities, amenities, parking charges
- **Efficient Processing**: Direct URL scraping with enhanced brand detection

### Web Interface
- **Interactive Dashboard**: Modern, responsive design with brand logos
- **Advanced Filtering**: Search by name, operator, motorway, food outlets, retail shops
- **Interactive Map**: Leaflet-powered map with station markers and clustering
- **Detailed Views**: Click stations for complete facility breakdown
- **Real-time Statistics**: Live filtering with dynamic counts
- **Mobile Responsive**: Optimized for all screen sizes

### Mobile Applications
- **Cross-Platform**: React Native app for iOS and Android
- **Station Discovery**: Browse and search all 102 service stations
- **Interactive Maps**: Native map integration with station markers
- **Offline Ready**: Local data storage for core functionality
- **Navigation Integration**: One-tap Google Maps navigation

## 📊 Current Dataset

- **102 Service Stations** (complete UK motorway coverage)
- **99% Scrape Success Rate** with real facilities data from operator websites
- **Comprehensive Facilities**: Food outlets, retail shops, amenities, parking charges
- **8 Operator Networks** with direct website integration
- **Precise Location Data**: GPS coordinates and motorway junction information

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
1. Open `index.html` in any modern web browser
2. The interface automatically loads data from `data/uk_service_stations.json`
3. Use advanced filtering by operator, food outlets, and amenities
4. Click stations for detailed facility breakdowns
5. Toggle between list view and interactive map

### Running from Project Root
```bash
# Start a simple HTTP server to avoid CORS issues
python -m http.server 8000

# Then visit: http://localhost:8000/
```

### Mobile App Development
```bash
# Navigate to mobile app directory
cd UKServiceStations

# Install dependencies
npm install

# Run on iOS (macOS only)
npm run ios

# Run on Android
npm run android
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

- **Regular Updates**: Automated scraping pipeline for data freshness
- **Enhanced Mobile Features**: Offline maps, push notifications, user favorites
- **API Development**: REST API endpoints for third-party integration
- **Analytics Dashboard**: Usage statistics and facility popularity metrics
- **Real-time Data**: Live parking availability and facility status updates

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is for educational and research purposes. Please respect the terms of service of the websites being scraped.

## 🙏 Acknowledgments

- Initial data source: GitHub CSV from charliejhadley/tidytuesday
- Live data sources: 8 major operator websites with real-time scraping
- Web technologies: Leaflet.js for mapping, Font Awesome for icons
- Mobile framework: React Native for cross-platform development
- Design inspiration: Modern responsive web and mobile design principles