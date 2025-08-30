import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import MapView, { Marker, Callout } from 'react-native-maps';
import { sampleServiceStations } from '../data/serviceStations';

const ServiceStationMap = ({ navigation }) => {
  const [stations, setStations] = useState([]);
  const [selectedStation, setSelectedStation] = useState(null);

  useEffect(() => {
    setStations(sampleServiceStations);
  }, []);

  const initialRegion = {
    latitude: 52.5,
    longitude: -1.5,
    latitudeDelta: 4,
    longitudeDelta: 4,
  };

  const renderMarker = (station) => (
    <Marker
      key={station.id}
      coordinate={{
        latitude: station.latitude,
        longitude: station.longitude,
      }}
      pinColor="#667eea"
      onPress={() => setSelectedStation(station)}
    >
      <Callout
        onPress={() => navigation.navigate('StationDetail', { station })}
      >
        <View style={styles.calloutContainer}>
          <Text style={styles.calloutTitle}>{station.name}</Text>
          <Text style={styles.calloutSubtitle}>{station.operator}</Text>
          <Text style={styles.calloutMotorway}>{station.motorway} • {station.direction}</Text>
          <Text style={styles.calloutFood}>
            🍔 {station.facilities.food_outlets.slice(0, 2).join(', ')}
          </Text>
          <Text style={styles.calloutTap}>Tap for details →</Text>
        </View>
      </Callout>
    </Marker>
  );

  return (
    <View style={styles.container}>
      <MapView
        style={styles.map}
        initialRegion={initialRegion}
        showsUserLocation={true}
        showsMyLocationButton={true}
      >
        {stations.map(renderMarker)}
      </MapView>
      
      {selectedStation && (
        <View style={styles.bottomSheet}>
          <TouchableOpacity
            style={styles.stationInfo}
            onPress={() => navigation.navigate('StationDetail', { station: selectedStation })}
          >
            <Text style={styles.selectedStationName}>{selectedStation.name}</Text>
            <Text style={styles.selectedStationDetails}>
              {selectedStation.operator} • {selectedStation.motorway}
            </Text>
            <Text style={styles.tapForDetails}>Tap for full details →</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    flex: 1,
  },
  calloutContainer: {
    width: 200,
    padding: 8,
  },
  calloutTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  calloutSubtitle: {
    fontSize: 12,
    color: '#667eea',
    marginBottom: 4,
  },
  calloutMotorway: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
  },
  calloutFood: {
    fontSize: 11,
    color: '#333',
    marginBottom: 4,
  },
  calloutTap: {
    fontSize: 10,
    color: '#667eea',
    fontStyle: 'italic',
  },
  bottomSheet: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: 'white',
    padding: 16,
    borderTopLeftRadius: 16,
    borderTopRightRadius: 16,
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  stationInfo: {
    alignItems: 'center',
  },
  selectedStationName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  selectedStationDetails: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  tapForDetails: {
    fontSize: 12,
    color: '#667eea',
    fontStyle: 'italic',
  },
});

export default ServiceStationMap;