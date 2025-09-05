import React from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  Image,
  Alert,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

import styles from './styles';
import ProfileCard from '../../components/CarteProfile/ProfileCard';
import MenuOption from '../../components/MenuOption/MenuOption';
import StatsRow from '../../components/LignesStatistiques/StatsRow';

import Mon_Header from '../../components/header';

const titre_de_mon_header = 'Profile';
export default function ProfileScreen({navigation}) {
  const profileData = {
    name: 'Mbabi Jeremy',
    email: 'jeremymbabi@email.com',
    phone: '+237 6 12 34 56 78',
    rating: 4.8,
    totalDeliveries: 1247,
    memberSince: 'Mars 2023',
    vehicle: 'Scooter Yamaha',
    avatar: 'https://media.licdn.com/dms/image/v2/D4E03AQGYNvl8MlKv8Q/profile-displayphoto-shrink_400_400/B4EZU5g4ISGYAg-/0/1740426712547?e=1758758400&v=beta&t=sTWWQ3a9k4ncYihEEfSViPGOsBXMd48UAbgQ96nV4jA',
  };

  const stats = [
    {label: 'Livraisons totales', value: '1,247'},
    {label: 'Note moyenne', value: '4.8/5'},
    {label: 'Taux de réussite', value: '98.5%'},
    {label: 'Temps moyen', value: '22 min'},
  ];

  const menuOptions = [
    {
      title: 'Informations personnelles',
      icon: 'person',
      onPress: () => {
        // Navigation vers écran d'édition du profil
        console.log('Informations personnelles');
      },
    },
    {
      title: 'Véhicule et documents',
      icon: 'directions-car',
      onPress: () => {
        // Navigation vers écran véhicule
        console.log('Véhicule et documents');
      },
    },
    {
      title: 'Historique des livraisons',
      icon: 'history',
      onPress: () => {
        // Navigation vers historique
        console.log('Historique des livraisons');
      },
    },
    {
      title: 'Paramètres de notification',
      icon: 'notifications',
      onPress: () => {
        // Navigation vers paramètres notifications
        console.log('Paramètres de notification');
      },
    },
    {
      title: 'Support client',
      icon: 'help',
      onPress: () => {
        // Navigation vers support
        console.log('Support client');
      },
    },
    {
      title: 'Conditions d\'utilisation',
      icon: 'description',
      onPress: () => {
        // Navigation vers conditions
        console.log('Conditions d\'utilisation');
      },
    },
    {
      title: 'Se déconnecter',
      icon: 'logout',
      onPress: () => {
        Alert.alert(
          'Déconnexion',
          'Êtes-vous sûr de vouloir vous déconnecter ?',
          [
            {text: 'Annuler', style: 'cancel'},
            {text: 'Déconnexion', onPress: () => navigation.replace('Login')},
          ]
        );
      },
      isDestructive: true,
    },
  ];

  return (
    <><Mon_Header titre_de_mon_header={titre_de_mon_header} /><ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Mon Profil</Text>
        <TouchableOpacity style={styles.editButton}>
          <Icon name="edit" size={20} color="#2563EB" />
        </TouchableOpacity>
      </View>

      <ProfileCard
        name={profileData.name}
        email={profileData.email}
        phone={profileData.phone}
        rating={profileData.rating}
        totalDeliveries={profileData.totalDeliveries}
        memberSince={profileData.memberSince}
        vehicle={profileData.vehicle}
        avatar={profileData.avatar} />

      <View style={styles.statsSection}>
        <Text style={styles.sectionTitle}>Statistiques</Text>
        {stats.map((stat, index) => (
          <StatsRow
            key={index}
            label={stat.label}
            value={stat.value} />
        ))}
      </View>

      <View style={styles.menuSection}>
        {menuOptions.map((option, index) => (
          <MenuOption
            key={index}
            title={option.title}
            icon={option.icon}
            onPress={option.onPress}
            isDestructive={option.isDestructive} />
        ))}
      </View>
    </ScrollView></>
  );
}
