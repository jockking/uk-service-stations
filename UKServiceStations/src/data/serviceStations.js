// Service stations data integration
export const loadServiceStations = async () => {
  try {
    // In a real app, this would fetch from your server or local bundle
    const response = await fetch('../data/uk_service_stations.json');
    const data = await response.json();
    return data.stations || [];
  } catch (error) {
    console.error('Error loading service stations:', error);
    return [];
  }
};

// Local data for development - subset of your actual data
export const sampleServiceStations = [
  {
    "id": 1,
    "name": "Baldock Services",
    "operator": "Extra MSA",
    "motorway": "A1(M)",
    "direction": "Both",
    "latitude": 51.9967,
    "longitude": -0.2019,
    "facilities": {
      "food_outlets": ["Greggs", "McDonald's"],
      "retail_shops": ["Marks & Spencer", "WHSmith"],
      "amenities": ["Baby Changing", "Cash Machine", "Dog Walking Area", "Parking", "Toilets"]
    }
  },
  {
    "id": 2,
    "name": "Birch Services",
    "operator": "Moto",
    "motorway": "M62",
    "direction": "Eastbound",
    "latitude": 53.5656,
    "longitude": -2.1845,
    "facilities": {
      "food_outlets": ["Burger King", "Costa Coffee"],
      "retail_shops": ["Marks & Spencer", "WHSmith"],
      "amenities": ["Baby Changing", "Cash Machine", "Dog Walking Area", "Parking", "Toilets"]
    }
  }
];

export const operators = [
  "Westmorland", "RoadChef", "Euro Garages", "Welcome Break", 
  "Stop 24", "Moto", "Extra MSA", "BP Connect"
];

export const foodOutlets = [
  "McDonald's", "Burger King", "KFC", "Subway", "Costa Coffee", 
  "Starbucks", "Greggs", "Leon", "Chopstix"
];

export const retailShops = [
  "WHSmith", "Marks & Spencer", "Waitrose & Partners", "Boots", "Tesco Express"
];