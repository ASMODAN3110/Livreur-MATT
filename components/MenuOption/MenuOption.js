import React from 'react';
import {TouchableOpacity, Text, View} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import styles from './styles';

export default function MenuOption({title, icon, onPress, isDestructive}) {
  return (
    <TouchableOpacity style={styles.container} onPress={onPress}>
      <View style={styles.leftSection}>
        <Icon 
          name={icon} 
          size={20} 
          color={isDestructive ? '#DC2626' : '#6B7280'} 
        />
        <Text style={[
          styles.title,
          isDestructive && styles.destructiveTitle
        ]}>
          {title}
        </Text>
      </View>
      <Icon name="chevron-right" size={20} color="#9CA3AF" />
    </TouchableOpacity>
  );
}

