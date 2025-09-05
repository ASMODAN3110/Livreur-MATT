import react from "react" ;
import {TouchableOpacity, Text} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import styles from './styles';

export default function ActionButton({ title , icon , backgroundColor , onPress, style}) {
  return (
    <TouchableOpacity
      style={[styles.container, {backgroundColor}, style]}
      onPress={onPress}>
      <Icon name={icon} size={20} color="#FFFFFF" />
      <Text style={styles.title}>{title}</Text>
    </TouchableOpacity>
  );
}