import React from 'react';
import {View, Text} from 'react-native';
import styles from './styles';

export default function EarningsChart({data}) {
  const maxAmount = Math.max(...data.map(item => item.amount));

  return (
    <View style={styles.container}>
      <View style={styles.chart}>
        {data.map((item, index) => {
          const height = (item.amount / maxAmount) * 100;
          return (
            <View key={index} style={styles.barContainer}>
              <View style={styles.barWrapper}>
                <View style={[styles.bar, {height: `${height}%`}]} />
              </View>
              <Text style={styles.dayLabel}>{item.day}</Text>
              <Text style={styles.amountLabel}>€{item.amount}</Text>
            </View>
          );
        })}
      </View>
    </View>
  );
}

