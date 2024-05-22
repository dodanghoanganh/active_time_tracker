from aqt import mw  # Import mw từ aqt
from aqt.qt import QDialog, QVBoxLayout, QLabel, QScrollArea, QWidget
from ..utils.active_time_tracker import ActiveTimeTracker

class HistoryView(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anki Usage History")
        self.layout = QVBoxLayout()

        self.history_label = QLabel("Anki Usage History")
        self.layout.addWidget(self.history_label)

        self.time_tracker = ActiveTimeTracker()
        stats = self.time_tracker.stats
        sessions = self.time_tracker.sessions

        history_content = ""
        for category, data in stats.items():
            history_content += f"\nCategory: {category}\n"
            for key, periods in data.items():
                name = ""
                if category == "decks":
                    name = mw.col.decks.name(key)
                elif category == "note_types":
                    name = mw.col.models.get(key)["name"]
                history_content += f"  {name} ({key}):\n"
                for period, time in periods.items():
                    if isinstance(time, (int, float)):
                        history_content += f"    {period}: {self.time_tracker.format_time(time)}\n"

        session_content = "\nSession History:\n"
        for session in sessions:
            # Ensure 'studied_cards' key exists in session
            if 'studied_cards' not in session:
                session['studied_cards'] = 0
            session_content += f"Start: {session['start_time']}, End: {session['end_time']}, Active Time: {self.time_tracker.format_time(session['active_time'])}, Studied Cards: {session['studied_cards']}\n"
            if session['active_time'] > 0:
                avg_study_time = session['active_time'] / session['studied_cards'] if session['studied_cards'] > 0 else 0
                session_content += f"    Average Cards/Hour: {session['studied_cards'] / (session['active_time'] / 3600):.2f}, Average Time/Card: {avg_study_time:.2f} seconds\n"

        self.history_content = QLabel(history_content + session_content)
        
        # Tạo một widget cuộn nếu nội dung dài hơn 15 dòng
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.addWidget(self.history_content)
        self.scroll_area.setWidget(self.scroll_content)

        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)
