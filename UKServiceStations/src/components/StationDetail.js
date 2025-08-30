import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Linking,
} from 'react-native';

const StationDetail = ({ route, navigation }) => {
  const { station } = route.params;

  const openMaps = () => {
    const url = `https://maps.google.com/?q=${station.latitude},${station.longitude}`;
    Linking.openURL(url);
  };

  const renderFacilitySection = (title, items, icon) => {
    if (!items || items.length === 0) return null;

    return (
      <View style={styles.facilitySection}>
        <Text style={styles.facilitySectionTitle}>
          {icon} {title}
        </Text>
        <View style={styles.facilityGrid}>
          {items.map((item, index) => (
            <View key={index} style={styles.facilityChip}>
              <Text style={styles.facilityChipText}>{item}</Text>
            </View>
          ))}
        </View>
      </View>
    );
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.stationName}>{station.name}</Text>
        <Text style={styles.operator}>{station.operator}</Text>
        <Text style={styles.location}>
          {station.motorway} • {station.direction}
        </Text>
      </View>

      <TouchableOpacity style={styles.navigationButton} onPress={openMaps}>
        <Text style={styles.navigationButtonText}>🗺️ Open in Maps</Text>
      </TouchableOpacity>

      <View style={styles.facilitiesContainer}>
        {renderFacilitySection(
          'Food Outlets',
          station.facilities.food_outlets,
          '🍔'
        )}

        {renderFacilitySection(
          'Retail Shops',
          station.facilities.retail_shops,
          '🛍️'
        )}

        {renderFacilitySection(
          'Amenities',
          station.facilities.amenities,
          '🚻'
        )}
      </View>

      <View style={styles.coordinatesContainer}>
        <Text style={styles.coordinatesTitle}>Coordinates</Text>
        <Text style={styles.coordinates}>
          {station.latitude.toFixed(4)}, {station.longitude.toFixed(4)}
        </Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#667eea',
    padding: 20,
    alignItems: 'center',
  },
  stationName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
    textAlign: 'center',
    marginBottom: 8,
  },
  operator: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.9)',
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
    marginBottom: 8,
  },
  location: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.8)',
  },
  navigationButton: {
    backgroundColor: '#4CAF50',
    margin: 16,
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  navigationButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  facilitiesContainer: {
    padding: 16,
  },
  facilitySection: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  facilitySectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 12,
  },
  facilityGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  facilityChip: {
    backgroundColor: '#f0f2ff',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 16,
    marginRight: 8,
    marginBottom: 8,
  },
  facilityChipText: {
    fontSize: 14,
    color: '#667eea',
    fontWeight: '500',
  },
  coordinatesContainer: {
    backgroundColor: 'white',
    margin: 16,
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  coordinatesTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  coordinates: {
    fontSize: 14,
    color: '#666',
    fontFamily: 'monospace',
  },
});

export default StationDetail;