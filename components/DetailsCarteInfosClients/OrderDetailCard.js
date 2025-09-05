import React from 'react';
import {View, Text, TouchableOpacity} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import styles from './styles';

const OrderDetailCard = ({ customerName,customerPhone,address,status,instructions}) => {
  const getStatusColor = () => {
    switch (status) {
      case 'en_cours':
        return '#2563EB';
      case 'en_attente':
        return '#EA580C';
      case 'livre':
        return '#059669';
      default:
        return '#6B7280';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'en_cours':
        return 'En cours de livraison';
      case 'en_attente':
        return 'En attente de prise en charge';
      case 'livre':
        return 'Livrée avec succès';
      default:
        return 'Statut inconnu';
    }
  };

  return (

    <View style={styles.container}>
      <View style={styles.statusBanner}>
        <View style={[styles.statusDot, {backgroundColor: getStatusColor()}]} />
        <Text style={[styles.statusText, {color: getStatusColor()}]}>
          {getStatusText()}
        </Text>
      </View>

      <View style={styles.customerSection}>
        <View style={styles.customerHeader}>
          <Icon name="person" size={20} color="#374151" />
          <Text style={styles.customerName}>{customerName}</Text>
        </View>
       
      </View>

      <View style={styles.addressSection}>
        <View style={styles.addressHeader}>
          <Icon name="location-on" size={20} color="#374151" />
          <Text style={styles.sectionTitle}>Adresse de livraison</Text>
        </View>
        <Text style={styles.addressText}>{address}</Text>
      </View>

      
    </View>
  );
}

export default OrderDetailCard