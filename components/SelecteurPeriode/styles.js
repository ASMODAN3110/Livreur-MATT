import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    backgroundColor: '#F3F4F6',
    borderRadius: 8,
    padding: 2,
  },
  periodButton: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
  },
  activePeriodButton: {
    backgroundColor: '#FFFFFF',
  },
  periodText: {
    fontSize: 12,
    color: '#6B7280',
    fontWeight: '500',
  },
  activePeriodText: {
    color: '#374151',
  },
});

export default styles ;