 import React, { useState, useRef, useEffect , useCallback } from 'react';
import { addresse_du_serveur } from '../../components/addresse_du_serveur';
import AsyncStorage from '@react-native-async-storage/async-storage';



export const Controlleur_De_La_Livraison = ({ navigation }) => {

  const { mon_addresse_ip, mon_numero_de_port } = addresse_du_serveur();
  const [identifiant_du_livreur, setIdLivreur] = useState(null);
  const [nom_du_livreur, setNomLivreur] = useState('');
  const [Le_Message_Du_Serveur, set_Le_Message_Du_Serveur] = useState('');
  const [Avertissement_Acceptation_De_Livraison, set_Avertissement_Acceptation_De_Livraison] = useState(false)
  const [Recuperation_success, set_Recuperation_success] = useState(false)
  const [Recuperation_failed, set_Recuperation_failed] = useState(false)
  const [Pas_acceptation_faite, set_Pas_acceptation_faite] = useState(false)
  const [Code_De_Recuperation_De_Commande,set_Code_De_Recuperation_De_Commande] = useState('') // cette variable va me permettre de contenir mon code de récupération de commande
  const [Bouton_De_Recuperation_De_Commande,set_Bouton_De_Recuperation_De_Commande] = useState(false) // cette variable va me permettre de savoir quand j ai appuyé sur le bouton qui me permet de signaler que j ai récupéré la commande dans le restaurant adéquat

  // maintenant moi je vais déclarer le useState qui va me permettre de garder l identifiant de la commande en cours

  const [identifiant_de_la_commande, set_identifiant_de_la_commande] = useState('') // ceci me permet de définir mon idenfiant de la commande qui est actuellement afficher
  const [id_de_la_redistribution, set_id_de_la_redistribution] = useState('') // ceci me permet de définir mon identiant de la redistribution

  const ws_envoi_de_l_etat_de_la_livraison = useRef(null);

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

    const ws = new WebSocket(`ws://${mon_addresse_ip}:${mon_numero_de_port}/envoi_de_l_etat_de_la_livraison/traiteur_de_livraison`);
    ws_envoi_de_l_etat_de_la_livraison.current = ws;

    ws.onopen = () => {
      //console.log(' WebSocket ouvert');

    };

    ws.onmessage = (event) => {

      try {

        const data = JSON.parse(event.data);
        //console.log(' Message reçu du serveur :', data);
        
        if (data.status === 'success' && data.action === 'redirection' ||
      data.status === 'update') {

          // set_Mon_Tableau_De_Commande_Journaliere(Mon_Tableau_De_Commande_Journaliere_inverser)  // recuperation de mon tableau contenant mes commandes du jour 

          // Set_Tableau_D_Info_Restaurant(data.Info_De_Mon_Restaurant);
          // ici je change la valeur de ma commande journaliere

          // j enleve les deux boutons qui sont là

          navigation.navigate('Main', {
            screen: 'Dashboard',
          
          });
          

        } else if (data.status === 'success' && data.action === 'pas_de_redirection') {

         // console.log(' Erreur dans les données reçues ou action non attendue');
         // afficher un popup qui dit qu un livreur est déjà positionner dessus
         set_Avertissement_Acceptation_De_Livraison(true)

        } else if (data.status === 'success' && data.action === 'recuperation_success') {

         // console.log(' Erreur dans les données reçues ou action non attendue');
         // afficher un popup qui dit qu un livreur est déjà positionner dessus
         // set_Avertissement_Acceptation_De_Livraison(true)
         set_Recuperation_success(true)
        } else if (data.status === 'success' && data.action === 'recuperation_failed') {

         // console.log(' Erreur dans les données reçues ou action non attendue');
         // afficher un popup qui dit qu un livreur est déjà positionner dessus
         // set_Avertissement_Acceptation_De_Livraison(true)
         set_Recuperation_failed(true)
        } else if (data.status === 'success' && data.action === 'pas_acceptation_faite') {

         // console.log(' Erreur dans les données reçues ou action non attendue');
         // afficher un popup qui dit qu un livreur est déjà positionner dessus
         // set_Avertissement_Acceptation_De_Livraison(true)
         set_Pas_acceptation_faite(true)
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
  }, []);

  const Accepter_La_Livraison = useCallback(() => {

      if (ws_envoi_de_l_etat_de_la_livraison.current?.readyState === WebSocket.OPEN) {

        const mes_donnees = {

            type: 'acceptation_de_la_livraison', // le type désignant la nature du websocket
            identifiant_du_livreur: parseInt(identifiant_du_livreur), // l identifiant du restaurant
            nom_du_livreur : nom_du_livreur ,  // le nom du restaurant
            id_de_la_redistribution : id_de_la_redistribution , // la redistribution sur laquelle je suis actuellement


        };

        //console.log(' Envoi des données :', mes_donnees);

        ws_envoi_de_l_etat_de_la_livraison.current?.send(JSON.stringify(mes_donnees));
  
       
        //console.log('Données de connexion envoyées');
      } else {
        //console.warn('WS /connexion pas prêt');
        setMessageServeur("Impossible d'établir la connexion au service. Veuillez réessayer plus tard.");
  
      }
  }, [identifiant_du_livreur, nom_du_livreur , identifiant_de_la_commande ]);


  const Recuperer_La_Livraison = useCallback((code) => {

      if (ws_envoi_de_l_etat_de_la_livraison.current?.readyState === WebSocket.OPEN) {

        const mes_donnees = {

            type: 'recuperation_de_la_livraison', // le type désignant la nature du websocket
            identifiant_du_livreur: parseInt(identifiant_du_livreur), // l identifiant du restaurant
            nom_du_livreur : nom_du_livreur ,  // le nom du restaurant
            id_de_la_redistribution : id_de_la_redistribution , // la redistribution sur laquelle je suis actuellement
            Code_De_Recuperation_De_Commande : code , // je récupère le code de récupération de la commande 


        };

        //console.log(' Envoi des données :', mes_donnees);

        ws_envoi_de_l_etat_de_la_livraison.current?.send(JSON.stringify(mes_donnees));
  
       
        //console.log('Données de connexion envoyées');
      } else {
        //console.warn('WS /connexion pas prêt');
        setMessageServeur("Impossible d'établir la connexion au service. Veuillez réessayer plus tard.");
  
      }
  }, [identifiant_du_livreur, nom_du_livreur , identifiant_de_la_commande ]);


  const Livrer_La_Livraison = useCallback((code) => {

      if (ws_envoi_de_l_etat_de_la_livraison.current?.readyState === WebSocket.OPEN) {

        const mes_donnees = {

            type: 'livrer_la_livraison', // le type désignant la nature du websocket
            identifiant_du_livreur: parseInt(identifiant_du_livreur), // l identifiant du restaurant
            nom_du_livreur : nom_du_livreur ,  // le nom du restaurant
            id_de_la_redistribution : id_de_la_redistribution , // la redistribution sur laquelle je suis actuellement
            Code_De_Recuperation_De_Commande : code , // je récupère le code de récupération de la commande 


        };

        //console.log(' Envoi des données :', mes_donnees);

        ws_envoi_de_l_etat_de_la_livraison.current?.send(JSON.stringify(mes_donnees));
  
       
        //console.log('Données de connexion envoyées');
      } else {
        //console.warn('WS /connexion pas prêt');
        setMessageServeur("Impossible d'établir la connexion au service. Veuillez réessayer plus tard.");
  
      }
  }, [identifiant_du_livreur, nom_du_livreur , identifiant_de_la_commande ]);
  
    
  return {

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
    
   
   
   
  };

};
