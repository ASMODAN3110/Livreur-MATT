import React, {useState, useEffect} from 'react';
import {View, Text, StyleSheet} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import styles from './styles';

export default function PriorityBar({orderTime}) {
  const [minutesElapsed, setMinutesElapsed] = useState(0);
  const [showPriority, setShowPriority] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      const orderDate = new Date(orderTime);
      const elapsed = Math.floor((now - orderDate) / (1000 * 60));
      
      setMinutesElapsed(elapsed);
      setShowPriority(elapsed >= 10); // Priorité après 10 minutes
    }, 60000); // Mise à jour chaque minute

    // Calcul initial
    const now = new Date();
    const orderDate = new Date(orderTime);
    const elapsed = Math.floor((now - orderDate) / (1000 * 60));
    setMinutesElapsed(elapsed);
    setShowPriority(elapsed >= 10);

    return () => clearInterval(interval);
  }, [orderTime]);

  if (!showPriority) {
    return null;
  }

  const getPriorityLevel = () => {
    if (minutesElapsed >= 30) return 'critique';
    if (minutesElapsed >= 20) return 'haute';
    return 'moyenne';
  };

  const getPriorityColor = () => {
    const level = getPriorityLevel();
    switch (level) {
      case 'critique': return '#DC2626';
      case 'haute': return '#EA580C';
      case 'moyenne': return '#F59E0B';
      default: return '#F59E0B';
    }
  };

  const getPriorityText = () => {
    const level = getPriorityLevel();
    switch (level) {
      case 'critique': return 'URGENT';
      case 'haute': return 'PRIORITÉ HAUTE';
      case 'moyenne': return 'PRIORITÉ';
      default: return 'PRIORITÉ';
    }
  };

  return (
    <View style={[styles.container, {backgroundColor: getPriorityColor()}]}>
      <Icon name="priority-high" size={16} color="#FFFFFF" />
      <Text style={styles.text}>
        {getPriorityText()} - {minutesElapsed} min
      </Text>
    </View>
  );
}

