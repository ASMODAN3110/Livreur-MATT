import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    height: 200,
  },
  chart: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'flex-end',
    height: 120,
    marginBottom: 16,
  },
  barContainer: {
    alignItems: 'center',
    flex: 1,
  },
  barWrapper: {
    height: 80,
    justifyContent: 'flex-end',
    marginBottom: 8,
  },
  bar: {
    backgroundColor: '#2563EB',
    width: 20,
    borderRadius: 4,
    minHeight: 4,
  },
  dayLabel: {
    fontSize: 12,
    color: '#6B7280',
    marginBottom: 2,
  },
  amountLabel: {
    fontSize: 10,
    color: '#374151',
    fontWeight: '500',
  },
});

export default styles ;