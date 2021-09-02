from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("ID Generator")
        self.source_dir = os.path.abspath(os.path.dirname(__file__))
        self.setWindowIcon(QIcon(os.path.join(self.source_dir, "logo/logo.jpg")))

        self.browser = QWebEngineView()
        self.browser.loadStarted.connect(self.loading)
        self.browser.loadFinished.connect(self.loading_finished)
        self.setCentralWidget(self.browser)
        self.load_html()
    
    def load_html(self):
        with open(os.path.join(self.source_dir,"renderer.html"), "r") as f:
            self.browser.setHtml(f.read(), QUrl.fromLocalFile(self.source_dir))
        print(self.source_dir)
    
    def loading_finished(self):
        print("Loading finished!")
    
    def loading(self):
        print("Loading...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()