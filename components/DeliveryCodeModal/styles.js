import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  modalContent: {
    width: '100%',
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 10,
    elevation: 5,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '700',
    marginBottom: 6,
  },
  modalSubtitle: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
  },
  codeInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 16,
    marginBottom: 16,
  },
  modalButtons: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
  },
  cancelButton: {
    paddingHorizontal: 14,
    paddingVertical: 10,
    marginRight: 8,
  },
  cancelButtonText: {
    fontSize: 16,
    color: '#333',
  },
  confirmButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 8,
  },
  confirmButtonText: {
    fontSize: 16,
    color: '#fff',
  },
});

export default styles
