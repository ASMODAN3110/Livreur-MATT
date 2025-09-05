import React, {useState} from 'react';
import { View,Text,TextInput,TouchableOpacity,Image,Alert} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import styles from './styles';
import {useConnexionController} from './controlleur'



const LoginScreen = ({navigation}) => {
  
  const  {
    email,
    setEmail,
    password,
    setPassword,
    messageServeur,
    showPassword, 
    setShowPassword ,
    seConnecter ,
  } = useConnexionController({navigation})


  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Image
          source={{uri: 'https://images.pexels.com/photos/4393021/pexels-photo-4393021.jpeg'}}
          style={styles.logo}
        />
        <Text style={styles.title}>MATT Livreurs</Text>
        <Text style={styles.subtitle}>{messageServeur}</Text>
      </View>

      <View style={styles.form}>
        <View style={styles.inputContainer}>
          <Icon name="email" size={20} color="#6B7280" style={styles.inputIcon} />
          <TextInput
            style={styles.input}
            placeholder="Email"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
          />
        </View> 

        <View style={styles.inputContainer}>
          <Icon name="lock" size={20} color="#6B7280" style={styles.inputIcon} />
          <TextInput
            style={styles.input}
            placeholder="Mot de passe"
            value={password}
            onChangeText={setPassword}
            secureTextEntry={!showPassword}
          />
          <TouchableOpacity
            onPress={() => setShowPassword(!showPassword)}
            style={styles.eyeIcon}>
            <Icon
              name={showPassword ? 'visibility' : 'visibility-off'}
              size={20}
              color="#6B7280"
            />
          </TouchableOpacity>
        </View>

        <TouchableOpacity style={styles.loginButton} onPress={seConnecter}>
          <Text style={styles.loginButtonText}>Se connecter</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.forgotPassword}>
          <Text style={styles.forgotPasswordText}>Mot de passe oublié ?</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

export default LoginScreen
