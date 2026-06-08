import sys
import os

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = './platforms'

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from ui.ecc import Ui_Dialog
import requests


class ECCApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Connect buttons to handlers
        self.ui.btn_generate.clicked.connect(self.call_api_generate)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_veryfi.clicked.connect(self.call_api_verify)

    def call_api_generate(self):
        url = "http://127.0.0.1:5000/ecc/generate"
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

    def call_api_sign(self):
        message = self.ui.txt_info.toPlainText().strip()
        if not message:
            QMessageBox.warning(self, "Warning", "Please enter a message to sign.")
            return

        url = "http://127.0.0.1:5000/ecc/sign"
        payload = {"message": message}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign.setPlainText(data["signature"])

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
        message = self.ui.txt_info.toPlainText().strip()
        signature = self.ui.txt_sign.toPlainText().strip()

        if not message or not signature:
            QMessageBox.warning(self, "Warning", "Please enter both message and signature.")
            return

        url = "http://127.0.0.1:5000/ecc/verify"
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
    window = ECCApp()
    window.show()
    sys.exit(app.exec_())
