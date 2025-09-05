import React from 'react';
import {View, Text, TouchableOpacity} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import PriorityBar from '../BarredePrioriter/PriorityBar';
import styles from './styles';

export default function RecentOrderCard({
  customerName,
  address,
  mattPoints,
  status,
  estimatedTime,
  orderTime,
  onPress,
}) {
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
        return 'En cours';
      case 'en_attente':
        return 'En attente';
      case 'livre':
        return 'Livrée';
      default:
        return 'Inconnu';
    }
  };

  return (
    <TouchableOpacity style={styles.container} onPress={onPress}>
      <PriorityBar orderTime={orderTime} />
      <View style={styles.header}>
        <Text style={styles.customerName}>{customerName}</Text>
        <Text style={styles.mattPoints}>{mattPoints}</Text>
      </View>
      
      <Text style={styles.address} numberOfLines={2}>
        {address}
      </Text>
      
      <View style={styles.footer}>
        <View style={styles.statusContainer}>
          <View style={[styles.statusDot, {backgroundColor: getStatusColor()}]} />
          <Text style={[styles.statusText, {color: getStatusColor()}]}>
            {getStatusText()}
          </Text>
        </View>
        <View style={styles.timeContainer}>
          <Icon name="schedule" size={16} color="#6B7280" />
          <Text style={styles.timeText}>{estimatedTime}</Text>
        </View>
      </View>
    </TouchableOpacity>
  );
}