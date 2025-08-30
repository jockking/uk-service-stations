# UK Service Stations Mobile App

A React Native mobile application for finding and exploring UK motorway service stations with detailed facility information and map integration.

## Features

- 📍 **Station List**: Browse all UK service stations with search and filtering
- 🗺️ **Interactive Map**: View stations on an interactive map with markers
- 🔍 **Smart Search**: Search by station name, motorway, or operator
- 🏢 **Detailed Info**: View complete facility information for each station
- 📱 **Cross Platform**: Works on both iOS and Android

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- React Native CLI
- iOS: Xcode 12+ and iOS Simulator
- Android: Android Studio with Android SDK

### Installation

1. Clone the repository and navigate to the mobile app:
```bash
cd UKServiceStations
npm install
```

2. For iOS (macOS only):
```bash
cd ios && pod install && cd ..
```

3. Start the Metro bundler:
```bash
npm start
```

4. Run on your preferred platform:
```bash
# iOS
npm run ios

# Android
npm run android
```

## Data Integration

The app uses your existing UK service stations data. To integrate your full dataset:

1. Copy your `uk_service_stations.json` file to `src/data/`
2. Update the data loading logic in `src/data/serviceStations.js`
3. The app currently includes sample data for development

## App Structure

```
src/
├── components/
│   ├── ServiceStationList.js    # Station list with filters
│   ├── MapView.js               # Interactive map component
│   └── StationDetail.js         # Station detail screen
└── data/
    └── serviceStations.js       # Data integration layer
```

## Key Features

### Station List
- Search by name or motorway
- Filter by operator (Moto, Welcome Break, etc.)
- Filter by food outlets (McDonald's, Costa, etc.)
- Responsive card-based layout

### Map View
- Interactive map with station markers
- Tap markers for quick info
- Navigate to full station details
- User location support

### Station Details
- Complete facility breakdown
- Food outlets, retail shops, and amenities
- One-tap navigation to Google Maps
- Responsive design

## Deployment

### iOS App Store
1. Configure app signing in Xcode
2. Build for release: `cd ios && xcodebuild -scheme UKServiceStations -configuration Release`
3. Upload to App Store Connect

### Google Play Store  
1. Generate signed APK: `cd android && ./gradlew assembleRelease`
2. Upload to Google Play Console

## Data Sources

Currently using sample data. To integrate your full dataset of 102+ UK service stations:
- Replace sample data with your JSON format
- Supports all major operators: Moto, Welcome Break, RoadChef, etc.
- Includes comprehensive facility data

## Contributing

This mobile app is designed to work with your existing UK service stations web platform and data scraping infrastructure.