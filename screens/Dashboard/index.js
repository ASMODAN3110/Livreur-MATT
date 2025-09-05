import React from 'react';
import {View,Text,ScrollView,TouchableOpacity,} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import styles from './styles'
import Mon_Header from '../../components/header/index'
import StatsCard from '../../components/CarteStats/StatsCard'
import RecentOrderCard from '../../components/CartesRecentes/RecentOrderCard';
import {Activeur_De_La_Recherche_Du_Tableau_De_Commande_A_Livrer} from './controlleur' ;


const titre_de_mon_header = 'Accueil';

const  DashboardScreen = ({navigation}) => {

  const {
    
    Le_Message_Du_Serveur ,
    nom_du_livreur ,
    Mon_Tableau_De_Commande_A_Livrer , 
    Mon_Tableau_De_Statistiques_Recentes ,
    Nombre_De_Commande_En_Attente_De_Livraison , 
    Mon_Tableau_De_Commande_En_Cours ,
   
  } =  Activeur_De_La_Recherche_Du_Tableau_De_Commande_A_Livrer({navigation})
  const statsData = [ 
    {
      title: 'Livraisons aujourd\'hui',
      value: '12',
      icon: 'local-shipping',
      color: '#2563EB',
      backgroundColor: '#EFF6FF',
    },
    {
      title: 'Gains du jour',
      value: '156 MATT',
      icon: 'attach-money',
      color: '#059669',
      backgroundColor: '#ECFDF5',
    },
    {
      title: 'Temps actif',
      value: '6h 30m',
      icon: 'schedule',
      color: '#EA580C',
      backgroundColor: '#FFF7ED',
    },
    {
      title: 'Note moyenne',
      value: '4.8',
      icon: 'star',
      color: '#DC2626',
      backgroundColor: '#FEF2F2',
    },
  ];


  return (
    <><Mon_Header titre_de_mon_header={titre_de_mon_header} /><ScrollView style={styles.container}>
      <View style={styles.header}>
        <View>
          <Text style={styles.greeting}>Bonjour,</Text>
          <Text style={styles.name}>{nom_du_livreur}</Text>
        </View>
        <TouchableOpacity style={styles.notificationButton}>
          <Icon name="notifications" size={24} color="#1F2937" />
          <View style={styles.notificationBadge}>
            <Text style={styles.notificationText}>{Nombre_De_Commande_En_Attente_De_Livraison}</Text>
          </View>
        </TouchableOpacity>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Statistiques du jour</Text>
        <View style={styles.statsGrid}>
          {statsData.map((stat, index) => (
            <StatsCard
              key={index}
              title={stat.title}
              value={stat.value}
              icon={stat.icon}
              color={stat.color}
              backgroundColor={stat.backgroundColor} />
          ))}
        </View>
      </View>

      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Mes Commandes En Cours</Text>
        </View>

        {Mon_Tableau_De_Commande_En_Cours.map((order) => (
          <RecentOrderCard
            key={order.id}
            customerName={order.customerName}
            address={order.address}
            mattPoints={order.mattPoints}
            status={order.status}
            estimatedTime={order.estimatedTime}
            orderTime={order.orderTime}
            onPress={() => navigation.navigate('OrderDetails', { order: order })} />
        ))}
      </View>

      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Commandes récentes</Text>
        </View>

        {Mon_Tableau_De_Commande_A_Livrer.map((order) => (
          <RecentOrderCard
            key={order.id}
            customerName={order.customerName}
            address={order.address}
            mattPoints={order.mattPoints}
            status={order.status}
            estimatedTime={order.estimatedTime}
            orderTime={order.orderTime}
            onPress={() => navigation.navigate('OrderDetails', { order: order })} />
        ))}
      </View>
    </ScrollView></>
  );
}

export default DashboardScreen