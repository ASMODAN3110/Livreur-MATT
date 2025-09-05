import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8FAFC',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    paddingTop: 20,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1F2937',
  },
  refreshButton: {
    padding: 8,
  },
  periodContainer: {
    flexDirection: 'row',
    paddingHorizontal: 20,
    marginBottom: 16,
  },
  periodButton: {
    flex: 1,
    paddingVertical: 12,
    paddingHorizontal: 16,
    marginHorizontal: 4,
    borderRadius: 8,
    backgroundColor: '#F3F4F6',
    alignItems: 'center',
  },
  activePeriodButton: {
    backgroundColor: '#2563EB',
  },
  periodText: {
    fontSize: 14,
    color: '#6B7280',
    fontWeight: '500',
  },
  activePeriodText: {
    color: '#FFFFFF',
  },
  ordersList: {
    flex: 1,
    paddingHorizontal: 20,
  },
});

export default styles ;