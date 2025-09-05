import React from 'react';
import {View, Text, StyleSheet, TouchableOpacity} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import styles from './styles';

export default function OrderCard({
  customerName,
  address,
  mattPoints,
  status,
  estimatedTime,
  distance,
  priority,
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

  const getPriorityColor = () => {
    return priority === 'haute' ? '#DC2626' : '#6B7280';
  };

  return (
    <TouchableOpacity style={styles.container} onPress={onPress}>
      {priority === 'haute' && (
        <View style={styles.priorityBanner}>
          <Icon name="priority-high" size={16} color="#FFFFFF" />
          <Text style={styles.priorityText}>Priorité haute</Text>
        </View>
      )}
      
      <View style={styles.header}>
        <View style={styles.customerInfo}>
          <Text style={styles.customerName}>{customerName}</Text>
        </View>
        <Text style={styles.mattPoints}>{mattPoints}</Text>
      </View>
      
      <View style={styles.addressContainer}>
        <Icon name="location-on" size={16} color="#6B7280" />
        <Text style={styles.address} numberOfLines={2}>
          {address}
        </Text>
      </View>
      
      <View style={styles.footer}>
        <View style={styles.statusContainer}>
          <View style={[styles.statusDot, {backgroundColor: getStatusColor()}]} />
          <Text style={[styles.statusText, {color: getStatusColor()}]}>
            {getStatusText()}
          </Text>
        </View>
        
        <View style={styles.infoContainer}>
          <View style={styles.infoItem}>
            <Icon name="schedule" size={14} color="#6B7280" />
            <Text style={styles.infoText}>{estimatedTime}</Text>
          </View>
          <View style={styles.infoItem}>
            <Icon name="navigation" size={14} color="#6B7280" />
            <Text style={styles.infoText}>{distance}</Text>
          </View>
        </View>
      </View>
    </TouchableOpacity>
  );
}
