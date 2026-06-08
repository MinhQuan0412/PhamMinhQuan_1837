import sys
import os
import binascii

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = './platforms'

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from ui.rsa import Ui_Dialog
from cipher.rsa.rsa_cipher import RSACipher
import requests


class RSAApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Connect buttons to handlers
        self.ui.btn_Ge.clicked.connect(self.call_api_generate)
        self.ui.btn_En.clicked.connect(self.call_api_encrypt)
        self.ui.btn_De.clicked.connect(self.call_api_decrypt)
        self.ui.btn_Sign.clicked.connect(self.call_api_sign)
        self.ui.btn_Ve.clicked.connect(self.call_api_verify)

    def call_api_generate(self):
        url = "http://127.0.0.1:5000/rsa/generate"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Keys generated successfully!")
                msg.exec_()
            else:
                data = response.json()
                QMessageBox.critical(self, "Error", data.get("error", "Unknown error"))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Cannot connect to API: {str(e)}")

    def call_api_encrypt(self):
        plain_text = self.ui.txt_Plain.toPlainText().strip()
        if not plain_text:
            QMessageBox.warning(self, "Warning", "Please enter plain text to encrypt.")
            return

        url = "http://127.0.0.1:5000/rsa/encrypt"
        payload = {"plain_text": plain_text}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_Cipher.setPlainText(data["cipher_text"])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encryption Successfully!")
                msg.exec_()
            else:
                data = response.json()
                QMessageBox.critical(self, "Error", data.get("error", "Unknown error"))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Cannot connect to API: {str(e)}")

    def call_api_decrypt(self):
        cipher_text = self.ui.txt_Cipher.toPlainText().strip()
        if not cipher_text:
            QMessageBox.warning(self, "Warning", "Please enter cipher text to decrypt.")
            return

        url = "http://127.0.0.1:5000/rsa/decrypt"
        payload = {"cipher_text": cipher_text}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_Plain.setPlainText(data["plain_text"])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decryption Successfully!")
                msg.exec_()
            else:
                data = response.json()
                QMessageBox.critical(self, "Error", data.get("error", "Unknown error"))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Cannot connect to API: {str(e)}")

    def call_api_sign(self):
        message = self.ui.txt_Info.toPlainText().strip()
        if not message:
            QMessageBox.warning(self, "Warning", "Please enter a message to sign.")
            return

        url = "http://127.0.0.1:5000/rsa/sign"
        payload = {"message": message}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_Sign.setPlainText(data["signature"])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Message signed successfully!")
                msg.exec_()
            else:
                data = response.json()
                QMessageBox.critical(self, "Error", data.get("error", "Unknown error"))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Cannot connect to API: {str(e)}")

    def call_api_verify(self):
        message = self.ui.txt_Info.toPlainText().strip()
        signature = self.ui.txt_Sign.toPlainText().strip()

        if not message or not signature:
            QMessageBox.warning(self, "Warning", "Please enter both message and signature.")
            return

        url = "http://127.0.0.1:5000/rsa/verify"
        payload = {"message": message, "signature": signature}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data.get("valid"):
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Signature is VALID!")
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Signature is INVALID!")
                    msg.exec_()
            else:
                data = response.json()
                QMessageBox.critical(self, "Error", data.get("error", "Unknown error"))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Cannot connect to API: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSAApp()
    window.show()
    sys.exit(app.exec_())
