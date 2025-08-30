import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  TextInput,
  ScrollView,
} from 'react-native';
import { sampleServiceStations, operators, foodOutlets } from '../data/serviceStations';

const ServiceStationList = ({ navigation }) => {
  const [stations, setStations] = useState([]);
  const [filteredStations, setFilteredStations] = useState([]);
  const [searchText, setSearchText] = useState('');
  const [selectedOperator, setSelectedOperator] = useState('');
  const [selectedFoodOutlet, setSelectedFoodOutlet] = useState('');

  useEffect(() => {
    setStations(sampleServiceStations);
    setFilteredStations(sampleServiceStations);
  }, []);

  useEffect(() => {
    filterStations();
  }, [searchText, selectedOperator, selectedFoodOutlet, stations]);

  const filterStations = () => {
    let filtered = stations;

    if (searchText) {
      filtered = filtered.filter(station =>
        station.name.toLowerCase().includes(searchText.toLowerCase()) ||
        station.motorway.toLowerCase().includes(searchText.toLowerCase())
      );
    }

    if (selectedOperator) {
      filtered = filtered.filter(station => station.operator === selectedOperator);
    }

    if (selectedFoodOutlet) {
      filtered = filtered.filter(station =>
        station.facilities.food_outlets.includes(selectedFoodOutlet)
      );
    }

    setFilteredStations(filtered);
  };

  const renderStation = ({ item }) => (
    <TouchableOpacity
      style={styles.stationCard}
      onPress={() => navigation.navigate('StationDetail', { station: item })}
    >
      <View style={styles.stationHeader}>
        <Text style={styles.stationName}>{item.name}</Text>
        <Text style={styles.operator}>{item.operator}</Text>
      </View>
      <Text style={styles.motorway}>{item.motorway} • {item.direction}</Text>
      <View style={styles.facilitiesContainer}>
        <Text style={styles.facilitiesTitle}>Food:</Text>
        <Text style={styles.facilities}>
          {item.facilities.food_outlets.slice(0, 2).join(', ')}
          {item.facilities.food_outlets.length > 2 ? '...' : ''}
        </Text>
      </View>
    </TouchableOpacity>
  );

  const FilterPicker = ({ title, options, selected, onSelect }) => (
    <View style={styles.filterContainer}>
      <Text style={styles.filterTitle}>{title}</Text>
      <ScrollView horizontal showsHorizontalScrollIndicator={false}>
        <TouchableOpacity
          style={[styles.filterChip, !selected && styles.filterChipSelected]}
          onPress={() => onSelect('')}
        >
          <Text style={[styles.filterChipText, !selected && styles.filterChipTextSelected]}>
            All
          </Text>
        </TouchableOpacity>
        {options.map((option) => (
          <TouchableOpacity
            key={option}
            style={[styles.filterChip, selected === option && styles.filterChipSelected]}
            onPress={() => onSelect(option)}
          >
            <Text style={[styles.filterChipText, selected === option && styles.filterChipTextSelected]}>
              {option}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.searchInput}
        placeholder="Search stations or motorways..."
        value={searchText}
        onChangeText={setSearchText}
      />

      <FilterPicker
        title="Operator"
        options={operators}
        selected={selectedOperator}
        onSelect={setSelectedOperator}
      />

      <FilterPicker
        title="Food Outlets"
        options={foodOutlets}
        selected={selectedFoodOutlet}
        onSelect={setSelectedFoodOutlet}
      />

      <Text style={styles.resultsCount}>
        {filteredStations.length} station{filteredStations.length !== 1 ? 's' : ''} found
      </Text>

      <FlatList
        data={filteredStations}
        renderItem={renderStation}
        keyExtractor={(item) => item.id.toString()}
        style={styles.list}
        showsVerticalScrollIndicator={false}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 16,
  },
  searchInput: {
    backgroundColor: 'white',
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  filterContainer: {
    marginBottom: 16,
  },
  filterTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
    color: '#333',
  },
  filterChip: {
    backgroundColor: 'white',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    marginRight: 8,
    borderWidth: 1,
    borderColor: '#667eea',
  },
  filterChipSelected: {
    backgroundColor: '#667eea',
  },
  filterChipText: {
    color: '#667eea',
    fontSize: 14,
  },
  filterChipTextSelected: {
    color: 'white',
  },
  resultsCount: {
    fontSize: 14,
    color: '#666',
    marginBottom: 16,
  },
  list: {
    flex: 1,
  },
  stationCard: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  stationHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  stationName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
  },
  operator: {
    fontSize: 12,
    color: '#667eea',
    backgroundColor: '#f0f2ff',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  motorway: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  facilitiesContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  facilitiesTitle: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#333',
    marginRight: 8,
  },
  facilities: {
    fontSize: 12,
    color: '#666',
    flex: 1,
  },
});

export default ServiceStationList;