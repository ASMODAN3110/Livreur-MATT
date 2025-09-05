import {StyleSheet} from 'react-native';

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    marginRight: 12,
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E5E7EB',
  },
  activeContainer: {
    backgroundColor: '#2563EB',
    borderColor: '#2563EB',
  },
  label: {
    fontSize: 14,
    color: '#374151',
    fontWeight: '500',
  },
  activeLabel: {
    color: '#FFFFFF',
  },
  count: {
    fontSize: 12,
    color: '#6B7280',
    marginLeft: 6,
    backgroundColor: '#F3F4F6',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 10,
    minWidth: 20,
    textAlign: 'center',
  },
  activeCount: {
    color: '#2563EB',
    backgroundColor: '#FFFFFF',
  },
});

export default styles ;