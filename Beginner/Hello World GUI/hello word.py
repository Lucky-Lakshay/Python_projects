import sys
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt

base_path = Path(__file__).parent
icon_path = base_path / "assets" / "icon.png"

class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My First GUI")
        self.setGeometry(700, 100, 500, 400)
        self.setWindowIcon(QIcon(str(icon_path)))
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        label1 = QLabel("Hello", self)
        label1.setFont(QFont("Arial", 30))
        label1.setStyleSheet("color:white;"
                            "background-color:pink;"
                            "font-weight:bold;")
        label1.setAlignment(Qt.AlignCenter)

        label2 = QLabel("World", self)
        label2.setFont(QFont("Arial", 30))
        label2.setStyleSheet("color:white;"
                            "background-color:green;"
                            "font-weight:bold;")
        label2.setAlignment(Qt.AlignCenter)
        
        grid = QGridLayout()
        grid.addWidget(label1, 0, 0)
        grid.addWidget(label2, 0, 1)
        central_widget.setLayout(grid)

def main():
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()