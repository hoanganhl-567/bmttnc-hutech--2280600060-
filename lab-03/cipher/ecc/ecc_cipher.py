import ecdsa
from PyQt5.QtWidgets import QMessageBox

class ECCCipher:
    def __init__(self):
        self.private_key = None
        self.public_key = None
    
    def generate_keys(self):
        try:
            self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST384p)
            self.public_key = self.private_key.get_verifying_key()
            return self.private_key, self.public_key
        except Exception as e:
            print(f"Error generating keys: {e}")
            raise e
    
    def set_keys(self, private_key, public_key):
        """ Cập nhật khóa từ bên ngoài (MyApp) """
        self.private_key = private_key
        self.public_key = public_key

    def sign_message(self, message):
        if self.private_key is None:
            raise ValueError("Private key is not set.")
        try:
            signature = self.private_key.sign(message.encode())
            return signature
        except Exception as e:
            print(f"Error signing message: {e}")
            raise e

    def verify_signature(self, message, signature):
        if self.public_key is None:
            raise ValueError("Public key is not set.")
        try:
            return self.public_key.verify(signature, message.encode())
        except ecdsa.BadSignatureError:
            return False
        except Exception as e:
            print(f"Error verifying signature: {e}")
            return False

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import QtWidgets
from ecc_ui import Ui_MainWindow
from ecc_cipher import ECCCipher

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ecc_cipher = ECCCipher()

        self.ui.pushButton.clicked.connect(self.handle_sign)
        self.ui.pushButton_2.clicked.connect(self.handle_verify)
        self.ui.pushButton_3.clicked.connect(self.handle_generate_keys)

    def handle_generate_keys(self):
        try:
            private_key, public_key = self.ecc_cipher.generate_keys()
            self.ecc_cipher.set_keys(private_key, public_key)  # Cập nhật khóa
            QMessageBox.information(self, "Keys Generated", "ECC keys generated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Key Generation Error", f"Error: {e}")

    def handle_sign(self):
        message = self.ui.lineEdit.text().strip()
        if not message:
            QMessageBox.warning(self, "Input Error", "Please enter text to sign.")
            return

        try:
            signature = self.ecc_cipher.sign_message(message)
            self.ui.lineEdit_2.setText(signature.hex())
            QMessageBox.information(self, "Python", "Signed successfully!")
        except ValueError as e:
            QMessageBox.warning(self, "Signing Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Signing Error", f"An error occurred: {e}")

    def handle_verify(self):
        message = self.ui.lineEdit.text().strip()
        signature_hex = self.ui.lineEdit_2.text().strip()

        if not message or not signature_hex:
            QMessageBox.warning(self, "Input Error", "Please enter both message and signature.")
            return

        try:
            signature = bytes.fromhex(signature_hex)
            is_valid = self.ecc_cipher.verify_signature(message, signature)

            if is_valid:
                QMessageBox.information(self, "Python", "Verified Successfully")
            else:
                QMessageBox.warning(self, "", "Verified Fail")
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Invalid signature format. Must be a hex string.")
        except Exception as e:
            QMessageBox.critical(self, "Verification Error", f"An error occurred: {e}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
