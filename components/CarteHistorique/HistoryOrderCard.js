import React from 'react';
import {View, Text, StyleSheet, TouchableOpacity} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import styles from './styles';

export default function HistoryOrderCard({
  customerName,
  address,
  mattPoints,
  deliveryDate,
  deliveryTime,
  onPress,
}) {
  return (
    <TouchableOpacity style={styles.container} onPress={onPress}>
      <View style={styles.header}>
        <Text style={styles.customerName}>{customerName}</Text>
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
          <View style={[styles.statusDot, {backgroundColor: '#059669'}]} />
          <Text style={[styles.statusText, {color: '#059669'}]}>
            Livrée
          </Text>
        </View>
        
        <View style={styles.dateContainer}>
          <Icon name="schedule" size={14} color="#6B7280" />
          <Text style={styles.dateText}>{deliveryDate} à {deliveryTime}</Text>
        </View>
      </View>
    </TouchableOpacity>
  );
}
