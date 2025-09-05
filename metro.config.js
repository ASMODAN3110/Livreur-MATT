const { getDefaultConfig, mergeConfig } = require('@react-native/metro-config');
const path = require('path');

const defaultConfig = getDefaultConfig(__dirname);

// ⚠️ On retire 'svg' de assetExts et on l’ajoute à sourceExts
defaultConfig.resolver.assetExts = defaultConfig.resolver.assetExts.filter(ext => ext !== 'svg');
defaultConfig.resolver.sourceExts = [...defaultConfig.resolver.sourceExts, 'svg'];

const config = {
  transformer: {
    babelTransformerPath: require.resolve('react-native-svg-transformer'),
  },
};

module.exports = mergeConfig(defaultConfig, config);

