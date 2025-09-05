import React, {useState,useEffect} from 'react';
import { View, Text , ScrollView , TouchableOpacity, Linking , Alert , Modal , TextInput} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import styles from './styles';
import OrderDetailCard from '../../components/DetailsCarteInfosClients/OrderDetailCard';
import ActionButton from '../../components/ActionBoutton/ActionButton';
import Titre_D_Un_Header from '../../components/titre_d_un_header';
import {Controlleur_De_La_Livraison} from './controlleur' ;
import Mon_PoPup from '../../components/popup';
import DeliveryCodeModal from '../../components/DeliveryCodeModal';




const OrderDetailsScreen = ({navigation, route}) => {
  const {order} = route.params;
  const mon_code_de_couleur = '#174feaff' 
  const titre_de_la_page = "Détails De La Commande"

  const [showModal, setShowModal] = useState(false);


    const {

      Le_Message_Du_Serveur ,
      set_Le_Message_Du_Serveur ,
      set_id_de_la_redistribution ,
      Accepter_La_Livraison , 
      Recuperer_La_Livraison ,
      Livrer_La_Livraison ,
      Avertissement_Acceptation_De_Livraison ,
      set_Avertissement_Acceptation_De_Livraison ,
      Recuperation_success ,
      set_Recuperation_success ,
      Recuperation_failed , 
      set_Recuperation_failed ,
      set_Code_De_Recuperation_De_Commande,
      Bouton_De_Recuperation_De_Commande,
      set_Bouton_De_Recuperation_De_Commande ,
      Pas_acceptation_faite ,
      set_Pas_acceptation_faite ,
     
    } = Controlleur_De_La_Livraison({navigation})

    const titre_du_popup = "livraison"
    const contenu_acceptation_livraison = " Cette commande à déjà été accepter , vous ne pouvez plus l acceptez"
    const contenu_recuperation_success = "récupération de la commande réussite"
    const contenu_recuperation_failed = " mot de passe erronée veuillez réessayer"
    const contenu_pas_acceptation_faite = "acceptez d abord la livraison avant de chercher a la récupérer"
    const texte_de_fermeture = "compris !"
   
  // identifiant_de_la_commande
  // Déplacer la mise à jour de l'identifiant ici
  useEffect(() => {
    set_id_de_la_redistribution(order["id_de_la_redistribution"])
  }, [order]);


  // données de la commande
  // order.id_de_la_redistribution
  const orderData = {
    id: order.id,
    customerName: order.customerName,
    customerPhone: order.customerPhone ,
    address: order.address ,
    items: order.items,
    mattPoints: order.mattPoints ,
    status: order.status ,
    localisation_du_restaurant : order.localisation_du_restaurant ,
   
  };

  const handleCall = () => {
    Linking.openURL(`tel:${orderData.customerPhone}`);
  };

  const Trouve_Un_Lieu = (nom_du_lieu) => {
    const url = `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(nom_du_lieu)}`;
    Linking.openURL(url);
  };

  return (
    <View style={styles.container}>
      
      <Titre_D_Un_Header navigation = {navigation} mon_titre = {titre_de_la_page} mon_code_de_couleur = {mon_code_de_couleur} />


      <ScrollView style={styles.content}>
        <OrderDetailCard 
          customerName={orderData.customerName}
          customerPhone={orderData.customerPhone}
          address={orderData.address}
          status={orderData.status}
        />

        <View style={styles.itemsSection}>
          <Text style={styles.sectionTitle}>Articles commandés</Text>
          {orderData.items.map((item, index) => (
            <View key={index} style={styles.itemRow}>
              <Text style={styles.itemName}>{item.name}</Text>
              <Text style={styles.itemQuantity}>x{item.quantity}</Text>
            </View>
          ))}
          
        </View>
        <View style={styles.actionButtons}>

        <ActionButton
          title="Accepter La Livraison"
          icon="local-shipping"
          backgroundColor="#f70707ff"
          onPress={Accepter_La_Livraison}
          style={styles.actionButton}
        />

        <ActionButton
          title="Navigation Vers Le Restaurant"
          icon="navigation"
          backgroundColor="#2563EB"
          onPress={() =>Trouve_Un_Lieu(order.localisation_du_restaurant)}
          style={styles.actionButton}
        />

         <ActionButton
          title="Navigation Vers Le Client"
          icon="navigation"
          backgroundColor="#831a9dff"
          onPress={() =>Trouve_Un_Lieu(order.address)}
          style={styles.actionButton}
        />

        <ActionButton
          title="Appeler"
          icon="phone"
          backgroundColor="#059669"
          onPress={handleCall}
          style={styles.actionButton}
        />
       
        <ActionButton
          title="Marquer livré"
          icon="check-circle"
          backgroundColor="#EA580C"
          onPress={handleCall}
          style={styles.fullWidthButton}
        />

        <ActionButton
          title="Marquer Récupéré"
          icon="restaurant"
          backgroundColor="#fc06cbff"
          onPress={() => setShowModal('sync')} // <-- ouvre le modal
          style={styles.fullWidthButton}
        />
      
        { Avertissement_Acceptation_De_Livraison && 

           <Mon_PoPup visible = {Avertissement_Acceptation_De_Livraison} setVisible = {set_Avertissement_Acceptation_De_Livraison} titre = {titre_du_popup} contenu = {contenu_acceptation_livraison} texte_de_fermeture = {texte_de_fermeture}  />

        }

        { Recuperation_success && 

           <Mon_PoPup visible = {Recuperation_success} setVisible = {set_Recuperation_success} titre = {titre_du_popup} contenu = {contenu_recuperation_success} texte_de_fermeture = {texte_de_fermeture}  />

        }

        { Recuperation_failed && 

           <Mon_PoPup visible = {Recuperation_failed} setVisible = {set_Recuperation_failed} titre = {titre_du_popup} contenu = {contenu_recuperation_failed} texte_de_fermeture = {texte_de_fermeture}  />

        }

        { Pas_acceptation_faite && 

           <Mon_PoPup visible = {Pas_acceptation_faite} setVisible = {set_Pas_acceptation_faite} titre = {titre_du_popup} contenu = {contenu_pas_acceptation_faite} texte_de_fermeture = {texte_de_fermeture}  />

        }

          

        { showModal === 'sync' && 

          <DeliveryCodeModal
              visible={showModal === 'sync'}
              onRequestClose={() => setShowModal(false)}
              title="Code de récupération de cette commande"                // texte configurable
              subtitle="Saisissez le code fourni par le restaurant"             // texte configurable
              placeholder="Entrez le code"                                  // placeholder configurable
              onConfirm={(code) => {
                 Recuperer_La_Livraison(code);      // <-- N'OUBLIE PAS les parenthèses pour appeler
                 setShowModal(false);
              }}
              onCancel={() => setShowModal(false)}
          />

        }

        


      </View>
      </ScrollView>

      
     
    </View>

  );
}

export default OrderDetailsScreen
