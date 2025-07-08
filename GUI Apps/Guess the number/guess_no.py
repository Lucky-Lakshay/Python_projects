import sys
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLineEdit, QPushButton, QFrame)
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette
from PyQt5.QtCore import Qt
from random import randint

base_path = Path(__file__).parent
icon_path = base_path / "assets" / "numbers.png"

class Guess_number_game(QWidget):
    def __init__(self):
        super().__init__()
        self.secret_number = randint(1, 100)
        self.attempt_count = 0
        self.max_attempts = 10
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Number Guessing Game")
        self.setWindowIcon(QIcon(str(icon_path)))
        
        # Set window background color
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)

        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title label
        self.title_label = QLabel("🎯 Number Guessing Game")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 15px;
                margin: 10px;
            }
        """)

        # Instructions label
        self.label = QLabel("🎲 Guess a number between 1 and 100:")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 16))
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                background: None;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
            }
        """)

        # Input field
        self.input = QLineEdit()
        self.input.setFont(QFont("Arial", 18))
        self.input.setAlignment(Qt.AlignCenter)
        self.input.setPlaceholderText("Enter your guess here...")
        self.input.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 3px solid #4CAF50;
                border-radius: 15px;
                padding: 12px;
                font-size: 18px;
                color: #333;
            }
            QLineEdit:focus {
                border: 3px solid #45a049;
                background: #f0f8ff;
            }
        """)
        
        # Connect Enter key to submit
        self.input.returnPressed.connect(self.check_guess)

        # Submit button
        self.button = QPushButton("🚀 Submit Guess")
        self.button.setFont(QFont("Arial", 16, QFont.Bold))
        self.button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4CAF50, stop:1 #45a049);
                color: white;
                border: none;
                border-radius: 15px;
                padding: 15px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #45a049, stop:1 #4CAF50);
            }
            QPushButton:pressed {
                background: #3d8b40;
            }
        """)
        self.button.clicked.connect(self.check_guess)

        # Result label
        self.result = QLabel("")
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setFont(QFont("Arial", 18, QFont.Bold))
        self.result.setStyleSheet("""
            QLabel {
                color: white;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
                min-height: 50px;
            }
        """)

        # Attempts counter
        self.attempts_label = QLabel(f"Attempts: {self.attempt_count}/{self.max_attempts}")
        self.attempts_label.setAlignment(Qt.AlignCenter)
        self.attempts_label.setFont(QFont("Arial", 14))
        self.attempts_label.setStyleSheet("""
            QLabel {
                color: white;
                background: None;
                border-radius: 8px;
                padding: 8px;
                margin: 5px;
            }
        """)

        # Reset button
        self.reset_button = QPushButton("🔄 New Game")
        self.reset_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.reset_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff7043, stop:1 #f4511e);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f4511e, stop:1 #ff7043);
            }
            QPushButton:pressed {
                background: #e64a19;
            }
        """)
        self.reset_button.clicked.connect(self.reset_game)

        # Add widgets to layout
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.input)
        main_layout.addWidget(self.button)
        main_layout.addWidget(self.result)
        main_layout.addWidget(self.attempts_label)
        main_layout.addWidget(self.reset_button)

        self.setLayout(main_layout)
        self.resize(450, 550)
        
        # Center the window on screen
        self.center_window()

    def center_window(self):
        """Center the window on the screen"""
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    def check_guess(self):
        try:
            guess = int(self.input.text())
            if guess < 1 or guess > 100:
                self.result.setText("⚠️ Please enter a number between 1 and 100!")
                self.result.setStyleSheet("""
                    QLabel {
                        color: #ffeb3b;
                        background: rgba(255, 235, 59, 0.2);
                        border: 2px solid #ffeb3b;
                        border-radius: 10px;
                        padding: 15px;
                        margin: 5px;
                        min-height: 50px;
                    }
                """)
                return
        except ValueError:
            self.result.setText("❌ Please enter a valid number!")
            self.result.setStyleSheet("""
                QLabel {
                    color: #f44336;
                    background: rgba(244, 67, 54, 0.2);
                    border: 2px solid #f44336;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 5px;
                    min-height: 50px;
                }
            """)
            return

        self.attempt_count += 1
        self.attempts_label.setText(f"Attempts: {self.attempt_count}/{self.max_attempts}")

        if guess < self.secret_number:
            self.result.setText("📈 Too low! Try a higher number.")
            self.result.setStyleSheet("""
                QLabel {
                    color: #2196F3;
                    background: rgba(33, 150, 243, 0.2);
                    border: 2px solid #2196F3;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 5px;
                    min-height: 50px;
                }
            """)
        elif guess > self.secret_number:
            self.result.setText("📉 Too high! Try a lower number.")
            self.result.setStyleSheet("""
                QLabel {
                    color: #FF9800;
                    background: rgba(255, 152, 0, 0.2);
                    border: 2px solid #FF9800;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 5px;
                    min-height: 50px;
                }
            """)
        else:
            self.result.setText(f"🎉 Congratulations! You guessed it in {self.attempt_count} attempts!")
            self.result.setStyleSheet("""
                QLabel {
                    color: #4CAF50;
                    background: rgba(76, 175, 80, 0.2);
                    border: 2px solid #4CAF50;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 5px;
                    min-height: 50px;
                }
            """)
            self.button.setEnabled(False)
            self.input.setEnabled(False)
            return

        # Check if max attempts reached
        if self.attempt_count >= self.max_attempts:
            self.result.setText(f"💀 Game Over! The number was {self.secret_number}. Try again!")
            self.result.setStyleSheet("""
                QLabel {
                    color: #f44336;
                    background: rgba(244, 67, 54, 0.2);
                    border: 2px solid #f44336;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 5px;
                    min-height: 50px;
                }
            """)
            self.button.setEnabled(False)
            self.input.setEnabled(False)

        # Clear input for next guess
        self.input.clear()
        self.input.setFocus()

    def reset_game(self):
        """Reset the game to start fresh"""
        self.secret_number = randint(1, 100)
        self.attempt_count = 0
        self.input.clear()
        self.input.setEnabled(True)
        self.button.setEnabled(True)
        self.result.setText("")
        self.result.setStyleSheet("""
            QLabel {
                color: white;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
                min-height: 50px;
            }
        """)
        self.attempts_label.setText(f"Attempts: {self.attempt_count}/{self.max_attempts}")
        self.input.setFocus()

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    game = Guess_number_game()
    game.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()