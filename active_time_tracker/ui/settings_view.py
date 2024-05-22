from aqt.qt import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
import json
import os
from ..utils.active_time_tracker import ActiveTimeTracker

class SettingsView(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cài đặt Active Time Tracker")
        self.layout = QVBoxLayout()

        self.idle_time_label = QLabel("Thời gian chờ không hoạt động:")
        self.layout.addWidget(self.idle_time_label)

        self.idle_time_combo = QComboBox()
        self.idle_time_combo.addItems(["15 giây", "30 giây", "1 phút", "5 phút", "10 phút", "15 phút"])
        self.layout.addWidget(self.idle_time_combo)

        self.save_button = QPushButton("Lưu cài đặt")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        self.load_settings()

    def load_settings(self):
        self.time_tracker = ActiveTimeTracker()
        idle_time = self.time_tracker.settings.get("idle_time", 60)
        index = [15, 30, 60, 300, 600, 900].index(idle_time)
        self.idle_time_combo.setCurrentIndex(index)

    def save_settings(self):
        idle_time_values = [15, 30, 60, 300, 600, 900]
        selected_idle_time = idle_time_values[self.idle_time_combo.currentIndex()]

        self.time_tracker.settings["idle_time"] = selected_idle_time
        self.time_tracker.save_settings()
        self.close()
