import React, {useState} from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Alert,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

import styles from './styles';
import Mon_Header from '../../components/header';

const titre_de_mon_header = 'Portefeuille';
export default function WalletScreen({navigation}) {
  const [selectedMethod, setSelectedMethod] = useState('orange');
  const [phoneNumber, setPhoneNumber] = useState('');

  const walletData = {
    mattPoints: '1,245 Points MATT',
    conversionRate: '1 Point MATT = 5 FCFA',
    availableBalance: '6,225 FCFA',
  };

  const paymentMethods = [
    {
      id: 'orange',
      name: 'Orange Money',
      icon: 'phone-android',
      color: '#FF6600',
    },
    {
      id: 'mtn',
      name: 'MTN Mobile Money',
      icon: 'phone-android',
      color: '#FFCC00',
    },
  ];

  const handleWithdraw = () => {
    if (!phoneNumber || phoneNumber.length < 8) {
      Alert.alert('Erreur', 'Veuillez saisir un numéro de téléphone valide');
      return;
    }

    Alert.alert(
      'Confirmation',
      `Effectuer un retrait vers le numéro ${phoneNumber} via ${
        paymentMethods.find(m => m.id === selectedMethod)?.name
      } ?`,
      [
        {text: 'Annuler', style: 'cancel'},
        {text: 'Confirmer', onPress: () => {
          Alert.alert('Succès', 'Demande de retrait envoyée avec succès');
          setPhoneNumber('');
        }},
      ]
    );
  };

  return (
    <>
      <Mon_Header titre_de_mon_header={titre_de_mon_header} />
      <ScrollView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}>
            <Icon name="arrow-back" size={24} color="#1F2937" />
          </TouchableOpacity>
          <Text style={styles.title}>Votre Portefeuille</Text>
          <View style={styles.placeholder} />
        </View>

        <View style={styles.balanceCard}>
          <View style={styles.balanceHeader}>
            <Icon name="account-balance-wallet" size={32} color="#2563EB" />
            <Text style={styles.balanceTitle}>Solde disponible</Text>
          </View>
          <Text style={styles.mattPoints}>{walletData.mattPoints}</Text>
          <Text style={styles.conversionRate}>{walletData.conversionRate}</Text>
          <Text style={styles.fcfaBalance}>≈ {walletData.availableBalance}</Text>
        </View>

        <View style={styles.withdrawSection}>
          <Text style={styles.sectionTitle}>Retirer mes gains</Text>

          <View style={styles.methodsContainer}>
            <Text style={styles.methodsLabel}>Méthode de paiement</Text>
            {paymentMethods.map((method) => (
              <TouchableOpacity
                key={method.id}
                style={[
                  styles.methodCard,
                  selectedMethod === method.id && styles.selectedMethod
                ]}
                onPress={() => setSelectedMethod(method.id)}>
                <View style={styles.methodInfo}>
                  <Icon name={method.icon} size={24} color={method.color} />
                  <Text style={styles.methodName}>{method.name}</Text>
                </View>
                <View style={[
                  styles.radioButton,
                  selectedMethod === method.id && styles.radioSelected
                ]} />
              </TouchableOpacity>
            ))}
          </View>

          <View style={styles.amountContainer}>
            <Text style={styles.amountLabel}>Numéro du bénéficiaire</Text>
            <TextInput
              style={styles.amountInput}
              placeholder="Ex: 699112233"
              value={phoneNumber}
              onChangeText={setPhoneNumber}
              keyboardType="phone-pad"
            />
          </View>

          <TouchableOpacity style={styles.withdrawButton} onPress={handleWithdraw}>
            <Text style={styles.withdrawButtonText}>Demander le retrait</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.historySection}>
          <Text style={styles.sectionTitle}>Historique des retraits</Text>
          <View style={styles.historyItem}>
            <View style={styles.historyInfo}>
              <Text style={styles.historyMethod}>Orange Money</Text>
              <Text style={styles.historyDate}>15 Nov 2024</Text>
            </View>
            <View style={styles.historyAmount}>
              <Text style={styles.historyValue}>-2,500 FCFA</Text>
              <Text style={styles.historyStatus}>Terminé</Text>
            </View>
          </View>
          <View style={styles.historyItem}>
            <View style={styles.historyInfo}>
              <Text style={styles.historyMethod}>MTN Mobile Money</Text>
              <Text style={styles.historyDate}>12 Nov 2024</Text>
            </View>
            <View style={styles.historyAmount}>
              <Text style={styles.historyValue}>-1,800 FCFA</Text>
              <Text style={styles.historyStatus}>Terminé</Text>
            </View>
          </View>
        </View>
      </ScrollView>
    </>
  );
}
