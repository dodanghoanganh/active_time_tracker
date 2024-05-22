from aqt.qt import QDialog, QVBoxLayout, QLabel
from ..utils.active_time_tracker import ActiveTimeTracker
import json
import os

class ReportView(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Báo cáo thời gian sử dụng Anki")
        self.layout = QVBoxLayout()

        self.report_label = QLabel("Báo cáo thời gian sử dụng Anki")
        self.layout.addWidget(self.report_label)

        # Tạo đối tượng ActiveTimeTracker để lấy dữ liệu
        self.time_tracker = ActiveTimeTracker()
        total_active_time = self.time_tracker.active_time
        deck_times = self.time_tracker.deck_times
        note_type_times = self.time_tracker.note_type_times
        profile_times = self.time_tracker.profile_times

        # Chuyển đổi thời gian từ giây sang định dạng đọc được
        total_time_str = self.time_tracker.format_time(total_active_time)
        deck_times_str = "\n".join([f"Deck {mw.col.decks.name(did)}: {self.time_tracker.format_time(time)}" for did, time in deck_times.items()])
        note_type_times_str = "\n".join([f"Note Type {mw.col.models.name(nid)}: {self.time_tracker.format_time(time)}" for nid, time in note_type_times.items()])
        profile_times_str = "\n".join([f"Profile {profile}: {self.time_tracker.format_time(time)}" for profile, time in profile_times.items()])

        # Hiển thị báo cáo thời gian sử dụng
        report_content = f"Thời gian sử dụng Anki: {total_time_str}\n\nThời gian theo từng deck:\n{deck_times_str}\n\nThời gian theo từng loại note:\n{note_type_times_str}\n\nThời gian theo từng profile:\n{profile_times_str}"
        self.report_content = QLabel(report_content)
        self.layout.addWidget(self.report_content)

        self.setLayout(self.layout)
