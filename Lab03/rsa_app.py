import sys
import os
import binascii

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = './platforms'

from PyQt5 import QtWidgets
from ui.rsa import Ui_Dialog
from cipher.rsa.rsa_cipher import RSACipher


class RSAApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.rsa = RSACipher()
        self.signature = None  # Lưu signature dạng bytes

        # Kết nối các nút với hàm xử lý
        self.ui.btn_Ge.clicked.connect(self.generate_keys)
        self.ui.btn_En.clicked.connect(self.encrypt_message)
        self.ui.btn_De.clicked.connect(self.decrypt_message)
        self.ui.btn_Sign.clicked.connect(self.sign_message)
        self.ui.btn_Ve.clicked.connect(self.verify_message)

    def generate_keys(self):
        try:
            self.rsa.generate_keys()
            self.ui.txt_Info.setPlainText('Keys generated successfully!\nPrivate & Public key saved to cipher/rsa/keys/')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def encrypt_message(self):
        plain_text = self.ui.txt_Plain.toPlainText().strip()
        if not plain_text:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Please enter plain text to encrypt.')
            return
        try:
            encrypted_bytes = self.rsa.encrypt(plain_text)
            # Hiển thị dạng hex để dễ đọc
            cipher_hex = binascii.hexlify(encrypted_bytes).decode('ascii')
            self.ui.txt_Cipher.setPlainText(cipher_hex)
            self.ui.txt_Info.setPlainText('Encryption successful!')
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Keys not found. Please generate keys first.')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def decrypt_message(self):
        cipher_hex = self.ui.txt_Cipher.toPlainText().strip()
        if not cipher_hex:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Please enter cipher text to decrypt.')
            return
        try:
            cipher_bytes = binascii.unhexlify(cipher_hex)
            plain_text = self.rsa.decrypt(cipher_bytes)
            self.ui.txt_Plain.setPlainText(plain_text)
            self.ui.txt_Info.setPlainText('Decryption successful!')
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Keys not found. Please generate keys first.')
        except binascii.Error:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Invalid cipher text format. Expected hex string.')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def sign_message(self):
        message = self.ui.txt_Info.toPlainText().strip()
        if not message:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Please enter a message to sign.')
            return
        try:
            self.signature = self.rsa.sign(message)
            # Hiển thị signature dạng hex
            sig_hex = binascii.hexlify(self.signature).decode('ascii')
            self.ui.txt_Sign.setPlainText(sig_hex)
            QtWidgets.QMessageBox.information(self, 'Success', 'Message signed successfully!')
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Keys not found. Please generate keys first.')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def verify_message(self):
        message = self.ui.txt_Info.toPlainText().strip()
        sig_hex = self.ui.txt_Sign.toPlainText().strip()

        if not message or not sig_hex:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Please enter a message and signature to verify.')
            return
        try:
            signature = binascii.unhexlify(sig_hex)
            result = self.rsa.verify(message, signature)
            if result:
                QtWidgets.QMessageBox.information(self, 'Result', 'Signature is VALID!')
            else:
                QtWidgets.QMessageBox.warning(self, 'Result', 'Signature is INVALID!')
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Keys not found. Please generate keys first.')
        except binascii.Error:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Invalid signature format. Expected hex string.')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', f'Verification failed: {str(e)}')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = RSAApp()
    window.show()
    sys.exit(app.exec_())
