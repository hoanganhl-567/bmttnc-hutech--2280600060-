import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Đúng với tên button trong file UI
        self.ui.pushButton.clicked.connect(self.call_api_encrypt)  # Encrypt
        self.ui.pushButton_2.clicked.connect(self.call_api_decrypt)  # Decrypt

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": self.ui.lineEdit.text(),  # Lấy dữ liệu từ QLineEdit
            "key": self.ui.lineEdit_2.text()
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.lineEdit_3.setText(data.get("encrypted_message", ""))  # Hiển thị kết quả
                self.show_message("Encryption Successful", "Encrypted Successfully", QMessageBox.Information)
            else:
                self.show_message("Encryption Error", f"API Error: {response.status_code}", QMessageBox.Warning)
        except requests.exceptions.RequestException as e:
            self.show_message("Request Failed", str(e), QMessageBox.Critical)

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": self.ui.lineEdit_3.text(),  # Lấy dữ liệu từ ô CipherText
            "key": self.ui.lineEdit_2.text()
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.lineEdit.setText(data.get("decrypted_message", ""))  # Hiển thị kết quả
                self.show_message("Decryption Successful", "Decrypted Successfully", QMessageBox.Information)
            else:
                self.show_message("Decryption Error", f"API Error: {response.status_code}", QMessageBox.Warning)
        except requests.exceptions.RequestException as e:
            self.show_message("Request Failed", str(e), QMessageBox.Critical)

    def show_message(self, title, text, icon):
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())