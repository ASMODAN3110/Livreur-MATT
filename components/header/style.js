import { StyleSheet , Dimensions} from "react-native";

const {width , height} = Dimensions.get('window')

const styles = StyleSheet.create({

    HeaderFirstPart : {


       
        flexDirection :"row" , 
        alignItems : "center" ,
        
        
       
    } , 

    logo : {

        width : width * 0.13,
        height : width * 0.13 , 
        borderRadius : (width * 0.4)/2 , 
        elevation : 0 ,
       
    } ,

    titre : {

      fontFamily : 'Inter Variable Text Thin' ,
      fontWeight : 'bold' , 
      fontSize : width * 0.05,
      color: '#2563EB',  // bleu electrique


    } ,

    Header : {
        flexDirection : 'row' ,
        backgroundColor : 'white' ,
        justifyContent : 'space-between' ,
        alignItems : 'center' ,
    }

  
   



})

export default styles 