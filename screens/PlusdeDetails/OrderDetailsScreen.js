import React from 'react';
import {View,Text,ScrollView,TouchableOpacity,Linking,} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import styles from './styles';

import OrderDetailCard from '../../components/DetailsCarteInfosClients/OrderDetailCard';
import ActionButton from '../../components/ActionBoutton/ActionButton';


import Mon_Header from '../../components/header';

const titre_de_mon_header = "Details"
export default function OrderDetailsScreen({navigation, route}) {
  const {orderId} = route.params;

  // Simulation des données de commande
  const orderData = {
    id: orderId,
    customerName: 'Marie',
    customerPhone: '+237 6 12 34 56 78',
    address: '15 Rue de la Paix, 75001 Douala',
    items: [
      {name: 'Pizza Margherita', quantity: 1},
      {name: 'Pizza 4 Fromages', quantity: 1},
      {name: 'Coca Cola 33cl', quantity: 2},
    ],

    deliveryFee: '25.02 Matt',
    status: 'en_cours',
    estimatedTime: '15 min',
    distance: '2.3 km',
    orderTime: '14:30',
    instructions: 'Sonner à l\'interphone, 3ème étage',
  };

  const handleCall = () => {
    Linking.openURL(`tel:${orderData.customerPhone}`);
  };

  const handleNavigate = () => {
    const url = `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(orderData.address)}`;
    Linking.openURL(url);
  };

  const handleMarkDelivered = () => {
    // Logique de marquage comme livré
    navigation.goBack();
  };

  return (
    <><Mon_Header titre_de_mon_header={titre_de_mon_header} /><View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}>
          <Icon name="arrow-back" size={24} color="#1F2937" />
        </TouchableOpacity>
        <Text style={styles.title}>Détails de la commande</Text>
        <View style={styles.placeholder} />
      </View>

      <ScrollView style={styles.content}>
        <OrderDetailCard
          customerName={orderData.customerName}
          customerPhone={orderData.customerPhone}
          address={orderData.address}
          orderTime={orderData.orderTime}
          estimatedTime={orderData.estimatedTime}
          distance={orderData.distance}
          status={orderData.status}
          instructions={orderData.instructions} />

        <View style={styles.itemsSection}>
          <Text style={styles.sectionTitle}>Articles commandés</Text>
          {orderData.items.map((item, index) => (
            <View key={index} style={styles.itemRow}>
              <Text style={styles.itemName}>{item.name}</Text>
              <Text style={styles.itemQuantity}>x{item.quantity}</Text>
            </View>
          ))}

          <View style={styles.totalSection}>
            <View style={styles.totalRow}>
              <Text style={styles.totalLabel}>Prix de livraison</Text>
              <Text style={styles.totalValue}>{orderData.deliveryFee}</Text>
            </View>
          </View>
        </View>

      <View style={styles.actionButtons}>
        <ActionButton
          title="Appeler"
          icon="phone"
          backgroundColor="#059669"
          onPress={handleCall}
          style={styles.actionButton} />
        <ActionButton
          title="Navigation"
          icon="navigation"
          backgroundColor="#2563EB"
          onPress={handleNavigate}
          style={styles.actionButton} />
        <ActionButton
          title="Marquer livré"
          icon="check-circle"
          backgroundColor="#EA580C"
          onPress={handleMarkDelivered}
          style={styles.fullWidthButton} />
      </View>
    </ScrollView>
        <View>
          <Text> </Text>
          <Text> </Text>
        </View>
    </View></>
  );
}
