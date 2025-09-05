import React, {useState} from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

import EarningsCard from '../../components/CartedeGains/EarningsCard';
import EarningsChart from '../../components/TableaudeGains/EarningsChart';
import PeriodSelector from '../../components/SelecteurPeriode/PeriodSelector';

import Mon_Header from '../../components/header';

import styles from './styles';


const titre_de_mon_header = 'Gains';
export default function EarningsScreen() {
  const [selectedWeek, setSelectedWeek] = useState('semaine1');

  const earningsData = {
    today: '156 Points MATT',
    week: '1,245 Points MATT',
    month: '4,890 Points MATT',
    total: '28,750 Points MATT',
  };

  const chartData = [
    {day: 'Lun', amount: 85},
    {day: 'Mar', amount: 92},
    {day: 'Mer', amount: 78},
    {day: 'Jeu', amount: 105},
    {day: 'Ven', amount: 120},
    {day: 'Sam', amount: 95},
    {day: 'Dim', amount: 67},
  ];

  const weeks = [
    {id: 'semaine1', label: 'Semaine 1 (1-7 Nov)'},
    {id: 'semaine2', label: 'Semaine 2 (8-14 Nov)'},
    {id: 'semaine3', label: 'Semaine 3 (15-21 Nov)'},
    {id: 'semaine4', label: 'Semaine 4 (22-28 Nov)'},
  ];

  const recentEarnings = [
    {
      id: '1',
      customerName: 'Marie Dubois',
      amount: '45 Points MATT',
      time: '14:30',
      type: 'livraison',
    },
    {
      id: '2',
      customerName: 'Jean Martin',
      amount: '32 Points MATT',
      time: '13:45',
      type: 'livraison',
    },
    {
      id: '3',
      customerName: 'Bonus performance',
      amount: '100 Points MATT',
      time: '12:00',
      type: 'bonus',
    },
  ];

  return (
    <><Mon_Header titre_de_mon_header={titre_de_mon_header} /><ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Mes Gains</Text>
      </View>

      <View style={styles.earningsGrid}>
        <EarningsCard
          title="Aujourd'hui"
          amount={earningsData.today}
          icon="today"
          color="#2563EB"
          backgroundColor="#EFF6FF" />
        <EarningsCard
          title="Cette semaine"
          amount={earningsData.week}
          icon="date-range"
          color="#059669"
          backgroundColor="#ECFDF5" />
        <EarningsCard
          title="Ce mois"
          amount={earningsData.month}
          icon="calendar-today"
          color="#EA580C"
          backgroundColor="#FFF7ED" />
        <EarningsCard
          title="Total"
          amount={earningsData.total}
          icon="account-balance-wallet"
          color="#7C3AED"
          backgroundColor="#F3E8FF" />
      </View>

      <View style={styles.chartSection}>
        <View style={styles.chartHeader}>
          <Text style={styles.sectionTitle}>Évolution des gains</Text>
        </View>

        <View style={styles.weekSelector}>
          {weeks.map((week) => (
            <TouchableOpacity
              key={week.id}
              style={[
                styles.weekButton,
                selectedWeek === week.id && styles.activeWeekButton,
              ]}
              onPress={() => setSelectedWeek(week.id)}>
              <Text
                style={[
                  styles.weekText,
                  selectedWeek === week.id && styles.activeWeekText,
                ]}>
                {week.label}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
        <EarningsChart data={chartData} />
      </View>

      <View style={styles.recentSection}>
        <Text style={styles.sectionTitle}>Gains récents</Text>
        {recentEarnings.map((earning) => (
          <View key={earning.id} style={styles.earningItem}>
            <View style={styles.earningInfo}>
              <Text style={styles.earningCustomer}>{earning.customerName}</Text>
              <Text style={styles.earningTime}>{earning.time}</Text>
            </View>
            <View style={styles.earningAmount}>
              <Text style={styles.earningValue}>+ {earning.amount}</Text>
              <View style={[
                styles.earningType,
                earning.type === 'bonus' && styles.bonusType
              ]}>
                <Text style={[
                  styles.earningTypeText,
                  earning.type === 'bonus' && styles.bonusTypeText
                ]}>
                  {earning.type === 'bonus' ? 'Bonus' : 'Livraison'}
                </Text>
              </View>
            </View>
          </View>
        ))}
      </View>
    </ScrollView></>
  );
}