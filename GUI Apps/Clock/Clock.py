import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QTimeEdit, QTabWidget, QSizePolicy, QStackedWidget
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl

base_path = Path(__file__).parent
icon_path = base_path / "assets" / "clock.png"

class ClockApp(QWidget): 
    def __init__(self):
        super().__init__()
        self.elapsed_time = 0
        self.alarm_time = None
        self.alarm_set = False
        self.alarm_triggered = False

        self.clock_timer = QTimer(self)
        self.stopwatch_timer = QTimer(self)

        # Alarm sound
        self.alarm_sound = QSoundEffect()
        alarm_sound_path = base_path / "assets" / "alarm.wav"
        if alarm_sound_path.exists():
            self.alarm_sound.setSource(QUrl.fromLocalFile(str(alarm_sound_path)))
            self.alarm_sound.setLoopCount(QSoundEffect.Infinite)
        else:
            print("⚠️ Warning: alarm.wav not found!")

        self.auto_stop_timer = QTimer(self)
        self.auto_stop_timer.setSingleShot(True)
        self.auto_stop_timer.timeout.connect(self.stop_alarm)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Clock App")
        self.setWindowIcon(QIcon(str(icon_path)))
        self.setGeometry(600, 300, 700, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #1c1b1b;
                color: white;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                font-size: 20px;
                padding: 10px;
                background-color: #333;
                color: white;
                border-radius: 8px;
                margin:30px 10px;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QTimeEdit {
                border:2px solid #333;
                font-size: 35px;
                padding: 10px;
                margin: 5px 10px;
            }
        """)

        main_layout = QVBoxLayout()

        # Top Clock
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 50px; font-family: Arial;margin:20px;")
        main_layout.addWidget(self.time_label)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #333;")
        main_layout.addWidget(line)

        # Tabs button
        tab_button_layout = QHBoxLayout()
        self.stopwatch_tab_btn = QPushButton("Stopwatch")
        self.alarm_tab_btn = QPushButton("Alarm")

        for btn in (self.stopwatch_tab_btn, self.alarm_tab_btn):
            btn.setCheckable(True)
            btn.setMinimumHeight(40)
            btn.setStyleSheet("font-size: 18px;")

        self.stopwatch_tab_btn.setChecked(True)  # default
        tab_button_layout.addWidget(self.stopwatch_tab_btn)
        tab_button_layout.addWidget(self.alarm_tab_btn)
        main_layout.addLayout(tab_button_layout)

        # --- Stacked widget
        self.stack = QStackedWidget()
        self.stopwatch_page = self.create_stopwatch_tab()
        self.alarm_page = self.create_alarm_tab()
        self.stack.addWidget(self.stopwatch_page)
        self.stack.addWidget(self.alarm_page)
        main_layout.addWidget(self.stack)

        #style tab buttons
        tab_style = """QPushButton {
                            border:2px solid #333;
                            border-radius:0px;
                            background-color: #999e9b;
                            color: #262525;
                            font-size: 35px;
                            margin:20px 0px;
                            padding:15px;
                        }
                        QPushButton:hover {
                            background-color: #787d7a;
                        }
                        QPushButton:checked {
                            background-color: #ffd166;  /* Highlight color for active tab */
                            color: #000;
                            border: 2px solid #555;
                        }"""
        self.stopwatch_tab_btn.setStyleSheet(tab_style)
        self.alarm_tab_btn.setStyleSheet(tab_style)

        # --- Button connections
        self.stopwatch_tab_btn.clicked.connect(self.show_stopwatch)
        self.alarm_tab_btn.clicked.connect(self.show_alarm)

        self.setLayout(main_layout)

        # Timers
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()

        self.stopwatch_timer.timeout.connect(self.update_stopwatch)

    def show_stopwatch(self):
        self.stack.setCurrentWidget(self.stopwatch_page)
        self.stopwatch_tab_btn.setChecked(True)
        self.alarm_tab_btn.setChecked(False)

    def show_alarm(self):
        self.stack.setCurrentWidget(self.alarm_page)
        self.alarm_tab_btn.setChecked(True)
        self.stopwatch_tab_btn.setChecked(False)

    def update_clock(self):
        now = QTime.currentTime()
        self.time_label.setText(now.toString("hh:mm:ss AP"))

        if self.alarm_set and not self.alarm_triggered and now >= self.alarm_time:
            self.alarm_status.setText("🔔 Alarm Ringing!")
            if self.alarm_sound.source().isValid() and not self.alarm_sound.isPlaying():
                self.alarm_sound.play()
                self.auto_stop_timer.start(60 * 1000)
            self.alarm_triggered = True

    def create_stopwatch_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.stopwatch_label = QLabel("00:00:00.00")
        self.stopwatch_label.setAlignment(Qt.AlignCenter)
        self.stopwatch_label.setStyleSheet("font-size: 60px; font-family: Arial;border:2px solid #333;")
        layout.addWidget(self.stopwatch_label)

        buttons = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.reset_button = QPushButton("Reset")

        self.start_button.clicked.connect(self.start_stopwatch)
        self.stop_button.clicked.connect(self.stop_stopwatch)
        self.reset_button.clicked.connect(self.reset_stopwatch)

        buttons.addWidget(self.start_button)
        buttons.addWidget(self.stop_button)
        buttons.addWidget(self.reset_button)

        layout.addLayout(buttons)
        widget.setLayout(layout)
        return widget

    def start_stopwatch(self):
        self.stopwatch_timer.start(10)

    def stop_stopwatch(self):
        self.stopwatch_timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def reset_stopwatch(self):
        sself.stopwatch_timer.stop()
        self.elapsed_time = 0
        self.stopwatch_label.setText("00:00:00.00")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_stopwatch(self):
        self.elapsed_time += 10
        self.stopwatch_label.setText(self.format_time(self.elapsed_time))

    def format_time(self, ms):
        h = ms // (3600 * 1000)
        m = (ms // (60 * 1000)) % 60
        s = (ms // 1000) % 60
        cs = (ms % 1000) // 10
        return f"{h:02}:{m:02}:{s:02}.{cs:02}"

    def create_alarm_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.alarm_time_edit = QTimeEdit()
        self.alarm_time_edit.setDisplayFormat("hh:mm AP")
        self.alarm_time_edit.setTime(QTime.currentTime())
        self.alarm_time_edit.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.alarm_time_edit)

        self.alarm_status = QLabel("No alarm set.")
        self.alarm_status.setAlignment(Qt.AlignCenter)
        self.alarm_status.setStyleSheet("font-size: 25px; color: #d3e0d7; border:2px solid #333;")
        layout.addWidget(self.alarm_status)

        button_layout = QHBoxLayout()
        self.set_alarm_button = QPushButton("Set Alarm")
        self.cancel_alarm_button = QPushButton("Cancel Alarm")
        self.stop_alarm_button = QPushButton("Stop Alarm") 

        self.set_alarm_button.clicked.connect(self.set_alarm)
        self.cancel_alarm_button.clicked.connect(self.cancel_alarm)
        self.stop_alarm_button.clicked.connect(self.stop_alarm)

        button_layout.addWidget(self.set_alarm_button)
        button_layout.addWidget(self.cancel_alarm_button)
        button_layout.addWidget(self.stop_alarm_button)
        layout.addLayout(button_layout)

        widget.setLayout(layout)
        return widget

    def set_alarm(self):
        selected_time = self.alarm_time_edit.time()
        now = QTime.currentTime()

        if selected_time <= now:
            self.alarm_status.setText("⚠️ Cannot set alarm in the past!")
            return

        self.alarm_time = selected_time
        self.alarm_set = True
        self.alarm_triggered = False
        self.alarm_status.setText(f"Alarm set for {self.alarm_time.toString('hh:mm AP')}")


    def stop_alarm(self):
        if self.alarm_sound.isPlaying():
            self.alarm_sound.stop()
        self.auto_stop_timer.stop()
        self.alarm_status.setText("Alarm stopped.")
        self.alarm_triggered = False

    def cancel_alarm(self):
        self.alarm_set = False
        self.alarm_triggered = False
        self.alarm_status.setText("Alarm canceled.")

def main():
    app = QApplication(sys.argv)
    Clock = ClockApp()
    Clock.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
