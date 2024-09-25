import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QWidget, QLineEdit, QLabel, QCheckBox, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap, QIcon
from endecryption import EncryptionEngine
import threading
import time

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class ListBoxWidget(QListWidget):
    def __init__(self, selectedLabel: QLabel, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(600, 600)

        self.selectedLabel = selectedLabel

    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        pixmap = QPixmap(resource_path("assets/dragndrop.png"))

        custom_width = 600
        custom_height = 600

        scaled_pixmap = pixmap.scaled(custom_width, custom_height, aspectRatioMode=1)

        x = (self.width() - custom_width) // 2
        y = (self.height() - custom_height) // 2

        painter.drawPixmap(x, y, scaled_pixmap.width(), scaled_pixmap.height(), scaled_pixmap)

        super().paintEvent(event)

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
            self.selectedLabel.setText(f"Selected file: {link}")
        else:
            event.ignore()


class EnkryptonUI(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__()
        self.resize(1200, 600)
        self.setWindowTitle("Enkrypton")
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))


        self.selectedLabel = QLabel("Selected file: ", self)
        self.selectedLabel.setAlignment(Qt.AlignCenter)
        self.selectedLabel.setStyleSheet("font-size: 15px")
        self.selectedLabel.setWordWrap(True)
        self.selectedLabel.setGeometry(700, 200, 460, 100)

        self.lstView = ListBoxWidget(selectedLabel=self.selectedLabel, parent=self)
        self.runBtn = QPushButton("Run!", self)
        self.runBtn.setGeometry(700, 500, 460, 50)
        self.runBtn.setFixedSize(460, 50)
        self.runBtn.clicked.connect(self.run)

        self.statusLabel = QLabel("", self)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setStyleSheet("font-size: 15px;")
        self.statusLabel.setWordWrap(True)
        self.statusLabel.setGeometry(700, 550, 460, 50)

        self.btnEncrypt = QCheckBox("Encrypt", self)
        self.btnEncrypt.setGeometry(950, 300, 100, 50)
        self.btnEncrypt.stateChanged.connect(lambda: self.btnDecrypt.setChecked(not self.btnEncrypt.isChecked()))

        self.btnDecrypt = QCheckBox("Decrypt", self)
        self.btnDecrypt.setGeometry(1060, 300, 100, 50)
        self.btnDecrypt.stateChanged.connect(lambda: self.btnEncrypt.setChecked(not self.btnDecrypt.isChecked()))

        self.pswdLabel = QLineEdit(self, placeholderText="Password")
        self.pswdLabel.setGeometry(700, 300, 200, 50)

        # Threadi
        self.stop_event = threading.Event() 

    def run(self):
        if (self.btnEncrypt.isChecked() and self.btnDecrypt.isChecked()) or (not self.btnEncrypt.isChecked() and not self.btnDecrypt.isChecked()):
            self.statusLabel.setText("Please select either Encrypt or Decrypt!")
            threading.Thread(target=self.resetStatus).start()
            return
        
        elif self.btnEncrypt.isChecked():
            self.encrypt()

        elif self.btnDecrypt.isChecked():
            self.decrypt()

    def encrypt(self):
        file_path = self.selectedLabel.text()
        password = self.pswdLabel.text()

        if not file_path or not password:
            self.statusLabel.setText("No file or password provided!")
            threading.Thread(target=self.resetStatus).start()
            return

        engine = EncryptionEngine(password)

        with open(resource_path(file_path), "rb") as f:
            file_data = f.read()

        encrypted_data = engine.encrypt(file_data)

        split_link = file_path.split(".")
        file_extension = split_link[-1]
        no_extension = ".".join(split_link[:-1])

        with open(resource_path(f"{no_extension}.eio"), "wb") as f:
            f.write(encrypted_data.encode('utf-8') + b"::" + file_extension.encode('utf-8'))
        
        self.statusLabel.setText("File encrypted successfully!")
        threading.Thread(target=self.resetStatus).start()

    def decrypt(self):
        file_path = self.selectedLabel.text()
        password = self.pswdLabel.text()

        if not file_path or not password:
            self.statusLabel.setText("No file or password provided!")
            threading.Thread(target=self.resetStatus).start()
            return

        if not file_path.endswith(".eio"):
            self.statusLabel.setText("File is not encrypted with Enrypton!")
            threading.Thread(target=self.resetStatus).start()
            return

        engine = EncryptionEngine(password)

        with open(resource_path(file_path), "rb") as f:
            encrypted_data = f.read()

        encrypted_content, file_extension = encrypted_data.rsplit(b"::", 1)
        decrypted_data = engine.decrypt(encrypted_content)

        no_extension = ".".join(file_path.split(".")[:-1])
        output_file = f"{no_extension}.{file_extension.decode()}"
        with open(resource_path(output_file), "wb") as f:
            f.write(decrypted_data)

        self.statusLabel.setText("File decrypted successfully!")
        threading.Thread(target=self.resetStatus).start()

    def resetStatus(self):
        time.sleep(3)
        self.statusLabel.setText("")

    def closeEvent(self, event):
        print("Closing window...")
        self.stop_event.set()

        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EnkryptonUI()
    window.show()


    sys.exit(app.exec_())
