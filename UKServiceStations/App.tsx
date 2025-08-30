import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar, Platform, Text } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import ServiceStationList from './src/components/ServiceStationList';
import ServiceStationMap from './src/components/MapView';
import StationDetail from './src/components/StationDetail';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

const ListStack = () => (
  <Stack.Navigator>
    <Stack.Screen 
      name="ServiceStationList" 
      component={ServiceStationList}
      options={{ title: 'Service Stations' }}
    />
    <Stack.Screen 
      name="StationDetail" 
      component={StationDetail}
      options={{ title: 'Station Details' }}
    />
  </Stack.Navigator>
);

const MapStack = () => (
  <Stack.Navigator>
    <Stack.Screen 
      name="ServiceStationMap" 
      component={ServiceStationMap}
      options={{ title: 'Map View' }}
    />
    <Stack.Screen 
      name="StationDetail" 
      component={StationDetail}
      options={{ title: 'Station Details' }}
    />
  </Stack.Navigator>
);

function App(): React.JSX.Element {
  return (
    <SafeAreaProvider>
      <NavigationContainer>
        <StatusBar 
          barStyle="light-content"
          backgroundColor="#667eea"
          translucent={Platform.OS === 'android'}
        />
        <Tab.Navigator
          screenOptions={{
            tabBarActiveTintColor: '#667eea',
            tabBarInactiveTintColor: 'gray',
            headerShown: false,
          }}
        >
          <Tab.Screen 
            name="List" 
            component={ListStack}
            options={{
              tabBarLabel: 'Stations',
              tabBarIcon: ({ color, size }) => (
                <Text style={{ color, fontSize: size }}>📍</Text>
              ),
            }}
          />
          <Tab.Screen 
            name="Map" 
            component={MapStack}
            options={{
              tabBarLabel: 'Map',
              tabBarIcon: ({ color, size }) => (
                <Text style={{ color, fontSize: size }}>🗺️</Text>
              ),
            }}
          />
        </Tab.Navigator>
      </NavigationContainer>
    </SafeAreaProvider>
  );
}

export default App;
