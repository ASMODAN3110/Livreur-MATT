import React, { useState, useEffect } from 'react';
import { Modal, View, Text, TextInput, TouchableOpacity } from 'react-native';
import styles from './styles';

/**
 * DeliveryCodeModal
 * Reusable modal with an input where you can set the title/subtitle and read the value entered.
 *
 * Props
 * - visible: boolean - show/hide modal
 * - onRequestClose: function - called when the modal should be closed (hardware back, overlay press if used)
 * - title: string - main title shown above the input
 * - subtitle: string - secondary text shown under the title
 * - placeholder: string - placeholder for TextInput
 * - value: string (optional) - if provided, the component becomes controlled
 * - onChangeText: function(text) (optional) - called when text changes (use with controlled mode)
 * - onConfirm: function(text) - called when the user taps the confirm button (receives the current text)
 *      - can be synchronous or return a Promise (async). If it returns a Promise, the component will await it when
 *        `autoCloseOnConfirm` is true.
 * - onCancel: function() (optional) - called when the user taps cancel
 * - confirmText / cancelText: strings (optional)
 * - maxLength / keyboardType: optional props forwarded to TextInput
 * - autoCloseOnConfirm: boolean (optional) - if true, the modal will call onRequestClose() after onConfirm completes.
 *
 * NOTE: keyboardType default is 'default' so the user can type any characters (letters, symbols, emoji...).
 */

const DeliveryCodeModal = ({
  visible,
  onRequestClose,
  title = 'Code',
  subtitle = '',
  placeholder = 'Entrez le code',
  value, // optional controlled value
  onChangeText, // optional controlled setter
  onConfirm,
  onCancel,
  confirmText = 'Confirmer',
  cancelText = 'Annuler',
  maxLength = 30,
  keyboardType = 'default', // allow any characters
  autoCloseOnConfirm = false,
}) => {
  const [internalCode, setInternalCode] = useState('');

  // keep internal state in sync if the parent clears the value (useful after confirm)
  useEffect(() => {
    if (typeof value !== 'undefined') return; // controlled mode -> don't touch internal
    // when modal opens, reset the internal code
    if (visible) setInternalCode('');
  }, [visible, value]);

  const isControlled = typeof value !== 'undefined';
  const code = isControlled ? value : internalCode;

  function handleChange(text) {
    if (isControlled) {
      onChangeText && onChangeText(text);
    } else {
      setInternalCode(text);
    }
  }

  async function handleConfirmPress() {
    if (!onConfirm) {
      // nothing to do, just close if requested
      onRequestClose && onRequestClose();
      return;
    }

    try {
      // call onConfirm; it can be sync or return a Promise
      const result = onConfirm(code);

      // if it returns a promise and autoCloseOnConfirm is true, await it
      if (autoCloseOnConfirm && result && typeof result.then === 'function') {
        await result;
      }

      // if user asked to auto-close, close now (works for sync and async)
      if (autoCloseOnConfirm) {
        onRequestClose && onRequestClose();
      }
    } catch (err) {
      // let parent handle errors if needed; just log here
      console.error('Error in onConfirm:', err);
    }
  }

  function handleCancelPress() {
    // if uncontrolled, clear internal value when cancelling
    if (!isControlled) setInternalCode('');
    onCancel && onCancel();
    onRequestClose && onRequestClose();
  }

  return (
    <Modal
      visible={visible}
      transparent={true}
      animationType="slide"
      onRequestClose={onRequestClose}
    >
      <View style={styles.modalOverlay}>
        <View style={styles.modalContent}>
          <Text style={styles.modalTitle}>{title}</Text>
          {subtitle ? <Text style={styles.modalSubtitle}>{subtitle}</Text> : null}

          <TextInput
            style={styles.codeInput}
            placeholder={placeholder}
            value={code}
            onChangeText={handleChange}
            keyboardType={keyboardType}
            maxLength={maxLength}
            // autoCapitalize and autoCorrect are left to parent if desired
          />

          <View style={styles.modalButtons}>
            <TouchableOpacity style={styles.cancelButton} onPress={handleCancelPress}>
              <Text style={styles.cancelButtonText}>{cancelText}</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.confirmButton} onPress={handleConfirmPress}>
              <Text style={styles.confirmButtonText}>{confirmText}</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );
}

export default DeliveryCodeModal
