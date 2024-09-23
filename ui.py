import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QWidget, QLineEdit
from PyQt5.QtCore import Qt, QUrl
import threading
import time
from endecryption import EncryptionEngine

#? https://www.youtube.com/watch?v=KVEIW2htw0A

class ListBoxWidget(QListWidget):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setAcceptDrops(True)   # Enable drop events for this widget
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
            #? print(link)
            self.link = link
        else:
            event.ignore()

    def getLink(self):
        return self.link


class EncriptonUI(QMainWindow):
    def __init__(self, parent: QWidget | None = ..., flags: Qt.WindowFlags | Qt.WindowType = ...) -> None:
        super().__init__()
        self.resize(1200, 600)
        self.windowTitle = "Encripton"

        self.lstView = ListBoxWidget(self)
        

        self.btn = QPushButton("Encrypt", self)
        self.btn.setGeometry(950, 300, 100, 50)
        self.btn.clicked.connect(self.encrypt)

        self.btn = QPushButton("Decrypt", self)
        self.btn.setGeometry(1060, 300, 100, 50)
        self.btn.clicked.connect(self.decrypt)

        self.pswdLabel = QLineEdit(self, placeholderText="Password")
        self.pswdLabel.setGeometry(700, 300, 200, 50)


    def encrypt(self):
        if self.lstView.getLink() is None or self.pswdLabel.text() == "":
            return
        else:
            engine = EncryptionEngine(self.pswdLabel.text())
            encrypted = engine.encrypt(self.lstView.getLink())
            split_link = self.lstView.getLink().split(".")
            no_extension = split_link[:-1][0]
            encrypted = encrypted + " " + split_link[-1] # zapise extension na konec
            with open(f"{no_extension}.eio", "w") as f:
                f.write(encrypted)

    def decrypt(self):
        if self.lstView.getLink() is None or self.pswdLabel.text() == "":
            return
        else:
            split_link = self.lstView.getLink().split(".")
            if split_link[-1] != "eio":
                return
            else:
                engine = EncryptionEngine(self.pswdLabel.text())
                with open(self.lstView.getLink(), "r") as f:
                    encrypted = f.read()
                    extension = encrypted.split(" ")[-1]
                    encrypted = encrypted.split(" ")[0]
                    decrypted = engine.decrypt(encrypted)
                    no_extension = split_link[:-1][0]
                    with open(no_extension + "." + extension, "w") as f:  # rekonstruira originalno ime datoteke
                        f.write(decrypted)
            



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = EncriptonUI()
    window.show()
    
    
    sys.exit(app.exec_())