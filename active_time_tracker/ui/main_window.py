from aqt.qt import QDialog, QVBoxLayout, QLabel, QPushButton
from .report_view import ReportView
from .settings_view import SettingsView
from .history_view import HistoryView
from ..utils.time_tracker import TimeTracker

class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Active Time Tracker")
        self.layout = QVBoxLayout()

        self.time_tracker = TimeTracker()
        self.overview_label = QLabel("Overview of Study Time")
        self.layout.addWidget(self.overview_label)

        self.report_button = QPushButton("View Report")
        self.report_button.clicked.connect(self.open_report_view)
        self.layout.addWidget(self.report_button)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings_view)
        self.layout.addWidget(self.settings_button)

        self.history_button = QPushButton("View History")
        self.history_button.clicked.connect(self.open_history_view)
        self.layout.addWidget(self.history_button)

        self.setLayout(self.layout)

    def open_report_view(self):
        self.report_view = ReportView()
        self.report_view.exec()

    def open_settings_view(self):
        self.settings_view = SettingsView()
        self.settings_view.exec()

    def open_history_view(self):
        self.history_view = HistoryView()
        self.history_view.exec()
