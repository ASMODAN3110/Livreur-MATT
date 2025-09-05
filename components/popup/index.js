import { View, Text , Pressable , Modal } from 'react-native'
import React from 'react'
import styles from './style'

const Mon_PoPup = ({visible , setVisible ,titre , contenu , texte_de_fermeture }) => {
  return (
    <View>

        <Modal

            visible = {visible} 
            animationType='fade'
            transparent = {true}
            onRequestClose={ () => setVisible(false)}
            
        >
            <View style = {styles.modalBackground}>

                <View style = {styles.modalContent}>

                    <Text style = {styles.title}>{titre}</Text>
                    <Text style = {styles.message}>{contenu}</Text>

                    <Pressable style = {styles.buttonClose} onPress={ ()=>setVisible(false)}>

                        <Text style = {styles.buttonText}>{texte_de_fermeture}</Text>

                    </Pressable>

                </View>

            </View>

        

        </Modal>
 
    </View>
  )
}

export default  Mon_PoPup