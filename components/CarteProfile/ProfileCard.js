import React from 'react';
import {View, Text, Image} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import styles from './styles';

export default function ProfileCard({
  name,
  email,
  phone,
  rating,
  totalDeliveries,
  memberSince,
  vehicle,
  avatar,
}) {
  return (
    <View style={styles.container}>
      <View style={styles.avatarSection}>
        <Image source={{uri: avatar}} style={styles.avatar} />
        <View style={styles.ratingContainer}>
          <Icon name="star" size={16} color="#FBBF24" />
          <Text style={styles.rating}>{rating}</Text>
        </View>
      </View>

      <View style={styles.infoSection}>
        <Text style={styles.name}>{name}</Text>
        <Text style={styles.email}>{email}</Text>
        <Text style={styles.phone}>{phone}</Text>
        
        <View style={styles.statsContainer}>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{totalDeliveries}</Text>
            <Text style={styles.statLabel}>Livraisons</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{memberSince}</Text>
            <Text style={styles.statLabel}>Membre depuis</Text>
          </View>
        </View>

        <View style={styles.vehicleContainer}>
          <Icon name="two-wheeler" size={16} color="#6B7280" />
          <Text style={styles.vehicleText}>{vehicle}</Text>
        </View>
      </View>
    </View>
  );
}
