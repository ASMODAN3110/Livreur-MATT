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
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1F2937',
  },
  historyButton: {
    padding: 8,
  },
  walletButton: {
    padding: 8,
  },
  earningsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    marginBottom: 24,
  },
  chartSection: {
    backgroundColor: '#FFFFFF',
    marginHorizontal: 20,
    marginBottom: 24,
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  chartHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  weekSelector: {
    marginBottom: 16,
  },
  weekButton: {
    paddingVertical: 8,
    paddingHorizontal: 12,
    marginBottom: 8,
    borderRadius: 6,
    backgroundColor: '#F3F4F6',
  },
  activeWeekButton: {
    backgroundColor: '#2563EB',
  },
  weekText: {
    fontSize: 14,
    color: '#6B7280',
    textAlign: 'center',
  },
  activeWeekText: {
    color: '#FFFFFF',
    fontWeight: '600',
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1F2937',
  },
  recentSection: {
    marginHorizontal: 20,
    marginBottom: 24,
  },
  earningItem: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  earningInfo: {
    flex: 1,
  },
  earningCustomer: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1F2937',
    marginBottom: 4,
  },
  earningTime: {
    fontSize: 14,
    color: '#6B7280',
  },
  earningAmount: {
    alignItems: 'flex-end',
  },
  earningValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#059669',
    marginBottom: 4,
  },
  earningType: {
    backgroundColor: '#EFF6FF',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  bonusType: {
    backgroundColor: '#FFF7ED',
  },
  earningTypeText: {
    fontSize: 12,
    color: '#2563EB',
    fontWeight: '500',
  },
  bonusTypeText: {
    color: '#EA580C',
  },
});

export default styles; 