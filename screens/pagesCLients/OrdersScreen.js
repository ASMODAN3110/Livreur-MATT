import React, {useState} from 'react';
import {View,Text,StyleSheet,ScrollView,TouchableOpacity,} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

import OrderCard from '../../components/CarteInfosClients/OrderCard';
import FilterButton from '../../components/FiltresBoutton/FilterButton';
import styles from './styles';
import Mon_Header from '../../components/header';

const titre_de_mon_header = "Commandes";

export default function OrdersScreen({navigation}) {
  const [activeFilter, setActiveFilter] = useState('toutes');

  const filters = [
    {id: 'toutes', label: 'Toutes', count: 4},
    {id: 'en_attente', label: 'En attente', count: 3},
    {id: 'en_cours', label: 'En cours', count: 1},
  ];

  const orders = [
    {
      id: '1',
      customerName: 'Marie',
      customerPhone: '+237 6 12 34 56 78',
      address: '15 Rue de la Paix, 75001 Douala',
      amount: '24.50 Matt',
      status: 'en_cours',
      estimatedTime: '15 min',
      distance: '2.3 km',
      priority: 'haute',
    },
    {
      id: '2',
      customerName: 'Jean ',
      customerPhone: '+237 6 98 76 54 32',
      address: '8 Avenue des Champs-Élysées, 75008 Douala',
      amount: '18.90 Matt',
      status: 'en_attente',
      estimatedTime: '25 min',
      distance: '1.8 km',
      priority: 'normale',
    },
    {
      id: '3',
      customerName: 'Laurent',
      customerPhone: '+237 6 11 22 33 44',
      address: '22 Boulevard Saint-Michel, 75005 Douala',
      amount: '31.20 Matt',
      status: 'en_attente',
      estimatedTime: '10min',
      distance: '3.1 km',
      priority: 'normale',
    },
    {
      id: '4',
      customerName: 'Daniel',
      customerPhone: '+237 6 55 66 77 88',
      address: '45 Rue de Rivoli, 75001 Douala',
      amount: '42.80 Matt',
      status: 'en_attente',
      estimatedTime: '20 min',
      distance: '1.2 km',
      priority: 'haute',
    },
  ];

  const filteredOrders = activeFilter === 'toutes' 
    ? orders 
    : orders.filter(order => order.status === activeFilter);

  return (

    <><Mon_Header titre_de_mon_header={titre_de_mon_header} /><View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity style={styles.refreshButton}>
          <Icon name="refresh" size={24} color="#2563EB" />
        </TouchableOpacity>
      </View>

      <View style={styles.filtersContainer}>
        {filters.map((filter) => (
          <FilterButton
            key={filter.id}
            label={filter.label}
            count={filter.count}
            isActive={activeFilter === filter.id}
            onPress={() => setActiveFilter(filter.id)} />
        ))}
      </View>


      <ScrollView style={styles.ordersList}>
        {filteredOrders.map((order) => (
          <OrderCard
            key={order.id}
            customerName={order.customerName}
            customerPhone={order.customerPhone}
            address={order.address}
            items={order.items}
            amount={order.amount}
            status={order.status}
            estimatedTime={order.estimatedTime}
            distance={order.distance}
            priority={order.priority}
            onPress={() => navigation.navigate('OrderDetails', { orderId: order.id })} />
        ))}
      </ScrollView>
    </View></>
  );
}
