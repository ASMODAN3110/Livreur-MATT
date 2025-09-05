import { useEffect, useRef, useState, useCallback } from 'react';
import { addresse_du_serveur } from '../../components/addresse_du_serveur';
import AsyncStorage from '@react-native-async-storage/async-storage';

export  const useConnexionController = ({navigation}) => {

  const [email, setEmail] = useState(''); // ceci me permet de déclarer mes emails
  const [password, setPassword] = useState(''); // ceci me permet de déclarer mon mot de passe
  const [showPassword, setShowPassword] = useState(false); // ceci me permet de déclarer ma variable qui décide de l état d affichage de mon mot de passe
  const [messageServeur, setMessageServeur] = useState('Connectez-vous à votre compte'); // ceci me permet d affficher un message d erreur du serveur



  const wsConnexion = useRef(null);

  const {
      
          mon_addresse_ip , 
          mon_numero_de_port ,
      
  } = addresse_du_serveur()

  useEffect(() => {
    wsConnexion.current = new WebSocket("ws://"+mon_addresse_ip+":"+mon_numero_de_port+"/livreurs_connexion/connexion") ; // création de mon websocket

    wsConnexion.current.onopen = () => {
      //console.log('WS /connexion ouvert'); mon websocket c est ouvert 
    };

    wsConnexion.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data); // WebSocket envoie TOUJOURS une string
        // console.log('/connexion →', data);

        if (data.status === "success" && data.action === "redirect") {

          const sauvegarderLivreur = async (id, nom) => {

            try {

              await AsyncStorage.setItem('id_livreur', id.toString())
              await AsyncStorage.setItem('nom_livreur',nom)

            } catch (error) {

                // errreur lors de l enregistrement des informations
            }

          }
          sauvegarderLivreur(data.identifiant_du_livreur,data.nom_du_livreur)
         navigation.navigate('Main', {
            screen: data.interface,
         });


        } else { 
          setMessageServeur(data.message);
        }
      } catch (err) {
       // console.error("Erreur de parsing JSON :", err);
       // console.error("Contenu reçu :", event.data);
       setMessageServeur("Impossible d'établir la connexion au service. Veuillez réessayer plus tard.");


      }
    };



    wsConnexion.current.onerror = (e) => {
      //console.error('WS /connexion erreur', e.message);
      setMessageServeur("Impossible d'établir la connexion au service. Veuillez réessayer plus tard.");

    };

    wsConnexion.current.onclose = () => {
      //console.log('WS /connexion fermé');
    };

    return () => {
      wsConnexion.current?.close();
    };
  }, [navigation]);

  const seConnecter = useCallback(() => {
    if (wsConnexion.current?.readyState === WebSocket.OPEN) {
      const payload = {
        type: 'connexion',
        email,
        password
      };

      wsConnexion.current.send(JSON.stringify(payload));
      //console.log('Données de connexion envoyées');
    } else {
      //console.warn('WS /connexion pas prêt');
      setMessageServeur("Impossible d'établir la connexion au service. Veuillez réessayer plus tard.");

    }
  }, [email, password]);

  return {
    email,
    setEmail,
    password,
    setPassword,
    messageServeur,
    showPassword, 
    setShowPassword ,
    seConnecter
  };
};
