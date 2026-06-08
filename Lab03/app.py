import sys
import os
import binascii

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = './platforms'

from PyQt5 import QtWidgets
from ui.ecc import Ui_Dialog
from cipher.ecc.ecc_cipher import ECCCipher

class ECCApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ecc = ECCCipher()
        self.signature = None  # Lưu signature dạng bytes

        # Kết nối các nút với hàm xử lý
        self.ui.btn_generate.clicked.connect(self.generate_keys)
        self.ui.btn_sign.clicked.connect(self.sign_message)
        self.ui.btn_veryfi.clicked.connect(self.verify_message)

    def generate_keys(self):
        try:
            self.ecc.generate_keys()
            QtWidgets.QMessageBox.information(self, 'Success', 'Keys generated successfully!')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def sign_message(self):
        message = self.ui.txt_info.toPlainText().strip()
        if not message:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Please enter a message to sign.')
            return
        try:
            sk, vk = self.ecc.load_keys()
            self.signature = self.ecc.sign(message, sk)
            # Hiển thị signature dạng hex
            sig_hex = binascii.hexlify(self.signature).decode('ascii')
            self.ui.txt_sign.setPlainText(sig_hex)
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Keys not found. Please generate keys first.')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def verify_message(self):
        message = self.ui.txt_info.toPlainText().strip()
        sig_hex = self.ui.txt_sign.toPlainText().strip()

        if not message or not sig_hex:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Please enter a message and signature to verify.')
            return
        try:
            signature = binascii.unhexlify(sig_hex)
            result = self.ecc.verify(message, signature, None)
            if result:
                QtWidgets.QMessageBox.information(self, 'Result', 'Signature is VALID!')
            else:
                QtWidgets.QMessageBox.warning(self, 'Result', 'Signature is INVALID!')
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Keys not found. Please generate keys first.')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', f'Verification failed: {str(e)}')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ECCApp()
    window.show()
    sys.exit(app.exec_())
