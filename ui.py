import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QWidget, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from endecryption import EncryptionEngine
import threading
import time

class ListBoxWidget(QListWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(600, 600)
        self.link = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            link = event.mimeData().urls()[0].toLocalFile()
            self.clear()
            self.addItem(QListWidgetItem(link))
            self.link = link
        else:
            event.ignore()

    def getLink(self):
        return self.link

class EnkryptonUI(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__()
        self.resize(1200, 600)
        self.setWindowTitle("Enkrypton")

        self.lstView = ListBoxWidget(self)

        self.selectedLabel = QLabel("Selected file: ", self)
        self.selectedLabel.setAlignment(Qt.AlignCenter)
        self.selectedLabel.setStyleSheet("font-size: 15px")
        self.selectedLabel.setWordWrap(True)
        self.selectedLabel.setGeometry(700, 200, 460, 100)

        self.statusLabel = QLabel("", self)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setStyleSheet("font-size: 15px")
        self.statusLabel.setWordWrap(True)
        self.statusLabel.setGeometry(700, 520, 460, 100)

        self.btnEncrypt = QPushButton("Encrypt", self)
        self.btnEncrypt.setGeometry(950, 300, 100, 50)
        self.btnEncrypt.clicked.connect(self.encrypt)

        self.btnDecrypt = QPushButton("Decrypt", self)
        self.btnDecrypt.setGeometry(1060, 300, 100, 50)
        self.btnDecrypt.clicked.connect(self.decrypt)

        self.pswdLabel = QLineEdit(self, placeholderText="Password")
        self.pswdLabel.setGeometry(700, 300, 200, 50)

        # Threadi
        self.stop_event = threading.Event() 
        self.update_thread = threading.Thread(target=self.updateLabel)

    def encrypt(self):
        file_path = self.lstView.getLink()
        password = self.pswdLabel.text()

        if not file_path or not password:
            return

        engine = EncryptionEngine(password)

        with open(file_path, "rb") as f:
            file_data = f.read()

        encrypted_data = engine.encrypt(file_data)

        split_link = file_path.split(".")
        file_extension = split_link[-1]
        no_extension = ".".join(split_link[:-1])

        with open(f"{no_extension}.eio", "wb") as f:
            f.write(encrypted_data.encode('utf-8') + b"::" + file_extension.encode('utf-8'))
        
        self.statusLabel.setText("File encrypted successfully!")
        threading.Thread(target=self.resetStatus).start()

    def decrypt(self):
        file_path = self.lstView.getLink()
        password = self.pswdLabel.text()

        if not file_path or not password:
            return

        if not file_path.endswith(".eio"):
            return

        engine = EncryptionEngine(password)

        with open(file_path, "rb") as f:
            encrypted_data = f.read()

        encrypted_content, file_extension = encrypted_data.rsplit(b"::", 1)
        decrypted_data = engine.decrypt(encrypted_content)

        no_extension = ".".join(file_path.split(".")[:-1])
        output_file = f"{no_extension}.{file_extension.decode()}"
        with open(output_file, "wb") as f:
            f.write(decrypted_data)

        self.statusLabel.setText("File decrypted successfully!")
        threading.Thread(target=self.resetStatus).start()

    def updateLabel(self):
        while not self.stop_event.is_set():
            self.selectedLabel.setText(f"Selected file: {self.lstView.getLink()}")
            time.sleep(0.5)

    def resetStatus(self):
        time.sleep(3)
        self.statusLabel.setText("")

    def closeEvent(self, event):
        print("Closing window...")
        self.stop_event.set()

        if self.update_thread.is_alive():
            self.update_thread.join()

        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EnkryptonUI()
    window.show()

    window.update_thread.start()  # Starta bg thread

    sys.exit(app.exec_())
