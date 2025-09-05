import React from 'react';
import {View, Text} from 'react-native';
import styles from './styles';

export default function StatsRow({label, value}) {
  return (
    <View style={styles.container}>
      <Text style={styles.label}>{label}</Text>
      <Text style={styles.value}>{value}</Text>
    </View>
  );
}
