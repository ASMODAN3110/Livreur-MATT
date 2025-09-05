import { View, Text , Image} from 'react-native'
import React from 'react'
import Icon from 'react-native-vector-icons/Ionicons';
import { Dimensions } from 'react-native';
import Ionicons from 'react-native-vector-icons/Ionicons'; // Import des icônes Ionicons
import styles from './style';

const { width } = Dimensions.get('window');


const Mon_Header = ({titre_de_mon_header}) => {

  
   // Définis ici les variables pour l’icône
  const focused = true; // ou false pour tester
  const size =  width * 0.08 ;

  const color = focused ? '#2563EB' : 'electric blue'; // bleu electrique 

  const iconName = focused ? 'settings' : 'settings-outline';


  return (

        <View style={styles.Header} >

            <View style={styles.HeaderFirstPart}>

            <Image source={require('../../assets/jpg/MattLogo.jpg')} style={styles.logo}/>
            <Text style={styles.titre}>{titre_de_mon_header}</Text>
        
            </View> 

        
            <View>
                {/* Ici l’icône avec nom, taille et couleur */}
            <Ionicons  name={iconName} size={size} color={color} />
            
            </View>


        </View>

  )

}

export default Mon_Header