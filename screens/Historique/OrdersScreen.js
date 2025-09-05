import React, {useState} from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

import styles from './styles';
import Mon_Header from '../../components/header';

import HistoryOrderCard from '../../components/CarteHistorique/HistoryOrderCard';


const titre_de_mon_header = 'Historique ';
export default function OrdersScreen({navigation}) {
  const [selectedPeriod, setSelectedPeriod] = useState('semaine');

  const historyOrders = [
    {
      id: '1',
      customerName: 'Marie Dubois',
      address: '15 Rue de la Paix, 75001 Paris',
      mattPoints: '45 Points MATT',
      status: 'livre',
      deliveryDate: '15 Nov 2024',
      deliveryTime: '14:30',
    },
    {
      id: '2',
      customerName: 'Jean Martin',
      address: '8 Avenue des Champs-Élysées, 75008 Paris',
      mattPoints: '32 Points MATT',
      status: 'livre',
      deliveryDate: '14 Nov 2024',
      deliveryTime: '16:45',
    },
    {
      id: '3',
      customerName: 'Sophie Laurent',
      address: '22 Boulevard Saint-Michel, 75005 Paris',
      mattPoints: '58 Points MATT',
      status: 'livre',
      deliveryDate: '13 Nov 2024',
      deliveryTime: '12:15',
    },
    {
      id: '4',
      customerName: 'Thomas Moreau',
      address: '45 Rue de Rivoli, 75001 Paris',
      mattPoints: '67 Points MATT',
      status: 'livre',
      deliveryDate: '12 Nov 2024',
      deliveryTime: '18:20',
    },
  ];

  const periods = [
    {id: 'semaine', label: 'Cette semaine'},
    {id: 'mois', label: 'Ce mois'},
    {id: 'Tout', label: 'Tout'},
  ];

  return (
    <><Mon_Header titre_de_mon_header={titre_de_mon_header} /><View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Consulter votre Historique</Text>
        <TouchableOpacity style={styles.refreshButton}>
          <Icon name="refresh" size={24} color="#2563EB" />
        </TouchableOpacity>
      </View>

      <View style={styles.periodContainer}>
        {periods.map((period) => (
          <TouchableOpacity
            key={period.id}
            style={[
              styles.periodButton,
              selectedPeriod === period.id && styles.activePeriodButton,
            ]}
            onPress={() => setSelectedPeriod(period.id)}>
            <Text
              style={[
                styles.periodText,
                selectedPeriod === period.id && styles.activePeriodText,
              ]}>
              {period.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <ScrollView style={styles.ordersList}>
        {historyOrders.map((order) => (
          <HistoryOrderCard
            key={order.id}
            customerName={order.customerName}
            address={order.address}
            mattPoints={order.mattPoints}
            deliveryDate={order.deliveryDate}
            deliveryTime={order.deliveryTime}
            /*onPress={() => navigation.navigate('OrderDetails', { orderId: order.id })}*/ /> /* mis en commentaire ; elle redirige vers la page des détails 
             à changer si besoin d'une redirection
            */
        ))}
      </ScrollView>
    </View></>
  );
}