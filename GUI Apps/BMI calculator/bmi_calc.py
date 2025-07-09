import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QComboBox, QGroupBox
)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt

base_path = Path(__file__).parent
icon_path = base_path / "assets" / "icon.png"
chart_path = base_path / "assets" / "chart.jpg"  # Make sure chart.jpg exists

class BMICalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.center()

    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        window = self.frameGeometry()
        window.moveCenter(screen.center())
        self.move(window.topLeft())

    def initUI(self):
        self.setWindowTitle("BMI Calculator")
        self.setWindowIcon(QIcon(str(icon_path)))
        self.setMinimumSize(600, 500)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        self.title_label = QLabel("BMI Calculator")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        main_layout.addWidget(self.title_label)

        # ==== Group Box for Input Section ====
        self.input_group = QGroupBox()
        self.input_group.setFont(QFont("Arial", 14))
        self.input_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #656b66;
                border-radius: 10px;
                margin-top: 10px;
                padding: 20px;
            }
        """)

        input_layout = QVBoxLayout()

        # Weight input
        weight_box = QHBoxLayout()
        self.weight_label = QLabel("Weight:")
        self.weight_label.setFont(QFont("Arial", 12))
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("e.g. 70")
        self.weight_input.setFont(QFont("Arial", 12))
        self.weight_unit = QComboBox()
        self.weight_unit.addItems(["kg", "lbs"])
        weight_box.addWidget(self.weight_label)
        weight_box.addWidget(self.weight_input)
        weight_box.addWidget(self.weight_unit)
        input_layout.addLayout(weight_box)

        # Height input
        height_box = QHBoxLayout()
        self.height_label = QLabel("Height:")
        self.height_label.setFont(QFont("Arial", 12))
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("e.g. 1.75")
        self.height_input.setFont(QFont("Arial", 12))
        self.height_unit = QComboBox()
        self.height_unit.addItems(["meters", "inches"])
        height_box.addWidget(self.height_label)
        height_box.addWidget(self.height_input)
        height_box.addWidget(self.height_unit)
        input_layout.addLayout(height_box)

        # Buttons
        button_box = QHBoxLayout()
        self.submit_button = QPushButton("Calculate BMI")
        self.submit_button.setFont(QFont("Arial", 12))
        self.submit_button.clicked.connect(self.calculate)
        self.reset_button = QPushButton("Reset")
        self.reset_button.setFont(QFont("Arial", 12))
        self.reset_button.clicked.connect(self.reset_fields)
        button_box.addWidget(self.submit_button)
        button_box.addWidget(self.reset_button)
        input_layout.addLayout(button_box)

        self.input_group.setLayout(input_layout)
        main_layout.addWidget(self.input_group)

        # ==== Result Label ====
        self.result = QLabel("")
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setFont(QFont("Courier New", 16, QFont.Bold))
        main_layout.addWidget(self.result)

        # ==== BMI Chart Image ====
        self.original_chart = QPixmap(str(chart_path))
        self.chart_label = QLabel()
        self.chart_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.chart_label)

        # ==== Tip ====
        tip = QLabel("Tip: Eat healthy and exercise regularly.")
        tip.setAlignment(Qt.AlignCenter)
        tip.setStyleSheet("color: #555; font-style: italic;")
        main_layout.addWidget(tip)

        self.weight_label.setFixedWidth(70)
        self.height_label.setFixedWidth(70)
        self.height_unit.setFixedWidth(70)
        self.weight_unit.setFixedWidth(70)

        self.setLayout(main_layout)
        self.update_chart_image()
        self.weight_input.setFocus()

    def resizeEvent(self, event):
        self.update_chart_image()
        super().resizeEvent(event)

    def update_chart_image(self):
        if not self.original_chart.isNull():
            target_width = int(self.width() * 0.5)
            scaled = self.original_chart.scaledToWidth(target_width, Qt.SmoothTransformation)
            self.chart_label.setPixmap(scaled)
        else:
            self.chart_label.setText("Chart image not found.")    

    def calculate(self):
        try:
            weight = float(self.weight_input.text())
            height = float(self.height_input.text())
            weight_unit = self.weight_unit.currentText()
            height_unit = self.height_unit.currentText()

            if weight <= 0:
                raise ValueError("Weight must be positive.")
            if height <= 0:
                raise ValueError("Height must be positive.")

            if weight_unit == "lbs":
                weight *= 0.453592
            if height_unit == "inches":
                height *= 0.0254

            bmi = weight / (height ** 2)

            if bmi < 18.5:
                category = "Underweight"
                color = "#3498db"
            elif bmi < 25:
                category = "Normal weight"
                color = "#2ecc71"
            elif bmi < 30:
                category = "Overweight"
                color = "#f39c12"
            else:
                category = "Obese"
                color = "#e74c3c"

            self.result.setText(f"Your BMI is: {bmi:.2f} ({category})")
            self.result.setStyleSheet(f"color: {color};")

        except ValueError as e:
            self.result.setText(f"Error: {str(e)}")
            self.result.setStyleSheet("color: #e74c3c;")
        except Exception:
            self.result.setText("Please enter valid numbers.")
            self.result.setStyleSheet("color: #e74c3c;")

    def reset_fields(self):
        self.weight_input.clear()
        self.height_input.clear()
        self.result.setText("")
        self.result.setStyleSheet("color: black;")
        self.weight_input.setFocus()

def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    window = BMICalculator()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
