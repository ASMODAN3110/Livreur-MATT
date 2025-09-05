import { StyleSheet } from "react-native";

const styles = StyleSheet.create({

    modalBackground: {
        flex: 1,
        backgroundColor: 'rgba(0,0,0,0.4)',
        justifyContent: 'center',
        alignItems: 'center',
    },

    modalContent: {
        backgroundColor: '#fff',
        width: '80%',
        padding: 20,
        borderRadius: 15,
        elevation: 10,
        alignItems: 'center',
    },

    title: {
        fontSize: 20,
        marginBottom: 10,
        fontWeight: 'bold',
        color : '#397655' , 
    },

    message: {
        fontSize: 16,
        marginBottom: 20,
    },


    buttonClose: {
        backgroundColor: '#397655',
        paddingVertical: 10,
        paddingHorizontal: 25,
        borderRadius: 10,
    },

    buttonText: {
        color: 'white',
        fontWeight: '600',
    },

   

})

export default styles 