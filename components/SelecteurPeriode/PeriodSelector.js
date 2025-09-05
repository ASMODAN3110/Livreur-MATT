import React from 'react';
import {View, TouchableOpacity, Text} from 'react-native';
import styles from './styles';

export default function PeriodSelector({periods, selectedPeriod, onSelect}) {
  return (
    <View style={styles.container}>
      {periods.map((period) => (
        <TouchableOpacity
          key={period.id}
          style={[
            styles.periodButton,
            selectedPeriod === period.id && styles.activePeriodButton,
          ]}
          onPress={() => onSelect(period.id)}>
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
  );
}

