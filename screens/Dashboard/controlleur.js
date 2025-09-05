 import React, { useState, useRef, useEffect } from 'react';
import { addresse_du_serveur } from '../../components/addresse_du_serveur';
import AsyncStorage from '@react-native-async-storage/async-storage';



export const Activeur_De_La_Recherche_Du_Tableau_De_Commande_A_Livrer = ({ navigation }) => {

  const { mon_addresse_ip, mon_numero_de_port } = addresse_du_serveur();

  const [identifiant_du_livreur, setIdLivreur] = useState(null);
  const [nom_du_livreur, setNomLivreur] = useState('');
  const [Le_Message_Du_Serveur, set_Le_Message_Du_Serveur] = useState('');
  const [Mon_Tableau_De_Commande_A_Livrer, set_Mon_Tableau_De_Commande_A_Livrer] = useState([]) // ceci représente le tableau ou seront stockés les informations de mon tableau de bord
  const [Mon_Tableau_De_Statistiques_Recentes, set_Mon_Tableau_De_Statistiques_Recentes] = useState([]) // ceci représente le tableau ou seront les données du livreur par rapport a certaines de ces statistiques
  const [Nombre_De_Commande_En_Attente_De_Livraison, set_Nombre_De_Commande_En_Attente_De_Livraison] = useState('') // ceci représente le nombre de commande qu il y a en attente actuellement qu il faut livrer
  const [Mon_Tableau_De_Commande_En_Cours, set_Mon_Tableau_De_Commande_En_Cours] = useState([])
  const ws_recherche_des_commandes_a_livrer = useRef(null);

  // Récupération de l'identifiant du restaurant depuis le stockage local

  useEffect(() => {

    const recupererInfos = async () => {

      const id = await AsyncStorage.getItem('id_livreur');
      const nom = await AsyncStorage.getItem('nom_livreur');

      if (id !== null) setIdLivreur(id);
      if (nom !== null) setNomLivreur(nom);

    };

    recupererInfos();

  }, [navigation]);

  // Connexion WebSocket
  useEffect(() => {

    const ws = new WebSocket(`ws://${mon_addresse_ip}:${mon_numero_de_port}/information_du_tableau_de_commande_a_livrer/recherche`);
    ws_recherche_des_commandes_a_livrer.current = ws;

    ws.onopen = () => {
      //console.log(' WebSocket ouvert');

      // Envoi immédiat après ouverture si l'ID est dispo
      if (identifiant_du_livreur) {

        const mes_donnees = {
          type: 'recherche_d_info_du_tableau_de_commande_a_livrer',
          identifiant_du_livreur: parseInt(identifiant_du_livreur),
          nom_du_livreur : nom_du_livreur , 
        };

        //console.log(' Envoi des données :', mes_donnees);

        ws.send(JSON.stringify(mes_donnees));

      } else {

       // console.log(' Identifiant du restaurant non défini au moment de l’ouverture');

      }

    };

    ws.onmessage = (event) => {

      try {
 
        const data = JSON.parse(event.data);
        //console.log(' Message reçu du serveur :', data);
        
        if (data.status === 'success' && data.action === 'affichage' ||
      data.status === 'update') {

           // set_Mon_Tableau_De_Commande_Journaliere(data.Mon_Tableau_De_Commande_Journaliere)  // recuperation de mon tableau contenant mes commandes du jour 

          // Set_Tableau_D_Info_Restaurant(data.Info_De_Mon_Restaurant);
          // ici je change la valeur de ma commande journaliere

          set_Nombre_De_Commande_En_Attente_De_Livraison(data.Nombre_De_Commande_En_Attente_De_Livraison) // ici je change le nombre de commande qu il faut livrer
          set_Mon_Tableau_De_Commande_A_Livrer(data.Mon_Tableau_De_Commande_A_Livrer) // ici je change le tableau de commande qu il y a en attente de livraison
          set_Mon_Tableau_De_Commande_En_Cours(data.Mon_Tableau_De_Commande_En_Cours) // ici je change le tableau que le livreur connecté doit livré

        } else {

         // console.log(' Erreur dans les données reçues ou action non attendue');

        }

      } catch (error) {

       // console.error(' Erreur lors du traitement du message du serveur :', error);
        // set_Le_Message_Du_Serveur('Erreur de traitement des données');

      }
    };

    ws.onerror = (e) => {
     // console.error(' WebSocket erreur :', e.message);
      //set_Le_Message_Du_Serveur('Erreur WebSocket');
    };

    ws.onclose = () => {
     // console.log('WebSocket fermé');
    };

    return () => {
      ws.close();
    };
  }, [mon_addresse_ip, mon_numero_de_port, identifiant_du_livreur]);

  return {
    
    Le_Message_Du_Serveur ,
    nom_du_livreur ,
    Mon_Tableau_De_Commande_A_Livrer , 
    Mon_Tableau_De_Statistiques_Recentes ,
    Nombre_De_Commande_En_Attente_De_Livraison,
    Mon_Tableau_De_Commande_En_Cours ,
   
  };
};
