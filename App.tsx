import React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {createStackNavigator} from '@react-navigation/stack';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import Icon from 'react-native-vector-icons/MaterialIcons';

import LoginScreen from './screens/connexion';
import DashboardScreen from './screens/Dashboard';
import OrdersScreen from './screens/Historique/OrdersScreen';
import OrderDetailsScreen from './screens/DetailsCommandes';
import EarningsScreen from './screens/Gains/EarningsScreen';
import WalletScreen from './screens/Convertisseur/WalletScreen';
import ProfileScreen from './screens/profile/ProfileScreen';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({route}) => ({
        tabBarIcon: ({focused, color, size}) => {
          let iconName;
          
          if (route.name === 'Dashboard') {
            iconName = 'dashboard';
          } else if (route.name === 'History') {
            iconName = 'history';
          } else if (route.name === 'Earnings') {
            iconName = 'attach-money';
          } else if (route.name === 'Profile') {
            iconName = 'person';
          } else if (route.name === 'Wallet') {
            iconName = 'currency-exchange';
          }
          
          return <Icon name={iconName ?? 'help-outline'} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#2563EB',
        tabBarInactiveTintColor: '#6B7280',
        headerShown: false,
      })}>
      <Tab.Screen 
        name="Dashboard" 
        component={DashboardScreen}
        options={{title: 'Accueil'}}
      />
      <Tab.Screen 
        name="History" 
        component={OrdersScreen}
        options={{title: 'Historique'}}
      />
      <Tab.Screen 
        name="Earnings" 
        component={EarningsScreen}
        options={{title: 'Gains'}}
      />
            <Tab.Screen 
        name="Wallet" 
        component={WalletScreen}
        options={{title: 'Convertisseur'}}
      />
      <Tab.Screen 
        name="Profile" 
        component={ProfileScreen}
        options={{title: 'Profil'}}
      />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{headerShown: false}}>
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Main" component={TabNavigator} />
        <Stack.Screen name="OrderDetails" component={OrderDetailsScreen} options={{ headerShown: true }}/>
        <Stack.Screen name="Wallet" component={WalletScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}