import { View, Text } from 'react-native'
import React , {useEffect} from 'react'

const Titre_D_Un_Header = ({navigation,mon_titre,mon_code_de_couleur}) => {
  
    useEffect(() =>{

        navigation.setOptions({
            title: mon_titre ,
            headerTitleStyle: {
                color: mon_code_de_couleur ,
            },
            headerTintColor: mon_code_de_couleur , // juste une couleur, pas un objet '#397655'
        });

    }, [])

}

export default Titre_D_Un_Header