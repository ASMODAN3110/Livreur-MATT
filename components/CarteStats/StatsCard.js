import React from 'react';
import {View, Text, StyleSheet} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import styles from './styles';
export default function StatsCard({title, value, icon, color, backgroundColor}) {
  return (
    <View style={[styles.container, {backgroundColor}]}>
      <View style={styles.iconContainer}>
        <Icon name={icon} size={24} color={color} />
      </View>
      <Text style={styles.value}>{value}</Text>
      <Text style={styles.title}>{title}</Text>
    </View>
  );
}
