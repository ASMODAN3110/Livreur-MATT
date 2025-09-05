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
    paddingTop: 15,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E5E7EB',
  },
  backButton: {
    padding: 8,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1F2937',
  },
  placeholder: {
    width: 40,
  },
  balanceCard: {
    backgroundColor: '#FFFFFF',
    margin: 20,
    padding: 24,
    borderRadius: 16,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  balanceHeader: {
    alignItems: 'center',
    marginBottom: 16,
  },
  balanceTitle: {
    fontSize: 16,
    color: '#6B7280',
    marginTop: 8,
  },
  mattPoints: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2563EB',
    marginBottom: 8,
  },
  conversionRate: {
    fontSize: 14,
    color: '#6B7280',
    marginBottom: 4,
  },
  fcfaBalance: {
    fontSize: 18,
    fontWeight: '600',
    color: '#059669',
  },
  withdrawSection: {
    backgroundColor: '#FFFFFF',
    margin: 20,
    marginTop: 0,
    padding: 20,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 16,
  },
  methodsContainer: {
    marginBottom: 20,
  },
  methodsLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 12,
  },
  methodCard: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#E5E7EB',
    marginBottom: 8,
  },
  selectedMethod: {
    borderColor: '#2563EB',
    backgroundColor: '#EFF6FF',
  },
  methodInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  methodName: {
    fontSize: 16,
    color: '#374151',
    marginLeft: 12,
  },
  radioButton: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: '#D1D5DB',
  },
  radioSelected: {
    borderColor: '#2563EB',
    backgroundColor: '#2563EB',
  },
  amountContainer: {
    marginBottom: 24,
  },
  amountLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 8,
  },
  amountInput: {
    borderWidth: 1,
    borderColor: '#D1D5DB',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    backgroundColor: '#FFFFFF',
  },
  pointsEquivalent: {
    fontSize: 12,
    color: '#6B7280',
    marginTop: 4,
  },
  withdrawButton: {
    backgroundColor: '#2563EB',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
  },
  withdrawButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  historySection: {
    backgroundColor: '#FFFFFF',
    margin: 20,
    marginTop: 0,
    padding: 20,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  historyItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#F3F4F6',
  },
  historyInfo: {
    flex: 1,
  },
  historyMethod: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1F2937',
  },
  historyDate: {
    fontSize: 14,
    color: '#6B7280',
    marginTop: 2,
  },
  historyAmount: {
    alignItems: 'flex-end',
  },
  historyValue: {
    fontSize: 16,
    fontWeight: '600',
    color: '#DC2626',
  },
  historyStatus: {
    fontSize: 12,
    color: '#059669',
    marginTop: 2,
  },
});

export default styles ;