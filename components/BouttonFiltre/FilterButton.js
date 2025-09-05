import React from 'react';
import {TouchableOpacity, Text} from 'react-native';
import styles from './styles';

export default function FilterButton({label, count, isActive, onPress}) {
  return (
    <TouchableOpacity
      style={[styles.container, isActive && styles.activeContainer]}
      onPress={onPress}>
      <Text style={[styles.label, isActive && styles.activeLabel]}>
        {label}
      </Text>
      <Text style={[styles.count, isActive && styles.activeCount]}>
        {count}
      </Text>
    </TouchableOpacity>
  );
}