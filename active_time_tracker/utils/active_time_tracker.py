import json
import os
import time
from datetime import datetime
from aqt import mw
from aqt.qt import QTimer
from aqt.utils import showInfo
from anki.hooks import addHook

class ActiveTimeTracker:
    def __init__(self):
        self.active_time = 0
        self.deck_times = {}
        self.note_type_times = {}
        self.profile_times = {}
        self.current_deck_id = None
        self.current_note_type = None
        self.current_profile = mw.pm.name
        self.last_active_time = time.time()
        self.total_studied_cards = 0
        self.session_studied_cards = 0
        self.sessions = []
        self.data_file = os.path.join(mw.pm.addonFolder(), "active_time_tracker", "data", "active_time_data.json")
        self.stats_file = os.path.join(mw.pm.addonFolder(), "active_time_tracker", "data", "stats.json")
        self.settings_file = os.path.join(mw.pm.addonFolder(), "active_time_tracker", "data", "settings.json")
        self.session_file = os.path.join(mw.pm.addonFolder(), "active_time_tracker", "data", "session_logs.json")
        self.settings = self.load_settings()
        self.check_interval = self.settings.get("idle_time", 60)
        
        self.load_data()
        self.load_stats()
        self.load_sessions()
        self.start_new_session()

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_activity)
        self.timer.start(1000)  # Check every second

        # Hook into deck and note type changes
        addHook("showDeck", self.on_deck_change)
        addHook("reviewCleanup", self.on_deck_change)
        addHook("unloadProfile", self.end_session)
        addHook("reviewCard", self.on_card_review)

    def check_activity(self):
        current_time = time.time()
        time_diff = current_time - self.last_active_time

        if time_diff < self.check_interval:
            self.active_time += 1
            self.update_stats(self.current_profile, 'profiles', self.active_time)
            if self.current_deck_id:
                self.update_stats(self.current_deck_id, 'decks', self.active_time)
            if self.current_note_type:
                self.update_stats(self.current_note_type, 'note_types', self.active_time)

        self.last_active_time = current_time
        self.save_data()
        self.save_stats()

    def on_card_review(self, card, ease):
        self.total_studied_cards = mw.col.db.scalar("SELECT COUNT() FROM revlog")
        self.session_studied_cards += 1
        self.save_data()

    def update_stats(self, key, category, active_time):
        if category not in self.stats:
            self.stats[category] = {}
        if key not in self.stats[category]:
            self.stats[category][key] = {
                'daily': {},
                'weekly': {},
                'monthly': {},
                'bi_monthly': {},
                'quarterly': {},
                'yearly': {}
            }
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        week_str = now.strftime("%Y-W%U")
        month_str = now.strftime("%Y-%m")
        bi_month_str = now.strftime("%Y-%m") if now.month % 2 == 0 else now.replace(month=now.month + 1).strftime("%Y-%m")
        quarter_str = f"{now.year}-Q{(now.month-1)//3+1}"
        year_str = now.strftime("%Y")

        self.update_time(self.stats[category][key]['daily'], date_str, active_time)
        self.update_time(self.stats[category][key]['weekly'], week_str, active_time)
        self.update_time(self.stats[category][key]['monthly'], month_str, active_time)
        self.update_time(self.stats[category][key]['bi_monthly'], bi_month_str, active_time)
        self.update_time(self.stats[category][key]['quarterly'], quarter_str, active_time)
        self.update_time(self.stats[category][key]['yearly'], year_str, active_time)

    def update_time(self, period_dict, period_str, active_time):
        if period_str not in period_dict:
            period_dict[period_str] = 0
        period_dict[period_str] += active_time

    def save_data(self):
        data = {
            "active_time": self.active_time,
            "deck_times": self.deck_times,
            "note_type_times": self.note_type_times,
            "profile_times": self.profile_times,
            "total_studied_cards": self.total_studied_cards,
            "last_saved_time": time.time()
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.active_time = data.get("active_time", 0)
                self.deck_times = data.get("deck_times", {})
                self.note_type_times = data.get("note_type_times", {})
                self.profile_times = data.get("profile_times", {})
                self.total_studied_cards = data.get("total_studied_cards", 0)

    def save_stats(self):
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f)

    def load_stats(self):
        if os.path.exists(self.stats_file):
            with open(self.stats_file, 'r') as f:
                self.stats = json.load(f)
        else:
            self.stats = {}

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        return {}

    def load_sessions(self):
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r') as f:
                self.sessions = json.load(f)
        else:
            self.sessions = []

    def save_sessions(self):
        with open(self.session_file, 'w') as f:
            json.dump(self.sessions, f, indent=4)

    def start_new_session(self):
        self.current_session = {
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": None,
            "active_time": 0,
            "studied_cards": 0
        }
        if not isinstance(self.sessions, list):
            self.sessions = []
        self.sessions.append(self.current_session)

    def end_session(self):
        if self.current_session:
            self.current_session["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.current_session["active_time"] = self.active_time
            self.current_session["studied_cards"] = self.session_studied_cards
            self.save_sessions()

    def on_deck_change(self, deck_id=None):
        if mw.col:
            self.current_deck_id = mw.col.decks.current()['id'] if mw.col.decks.current() else None
            self.current_note_type = mw.col.models.current()['id'] if mw.col.models.current() else None

    def format_time(self, seconds):
        hrs, secs = divmod(seconds, 3600)
        mins, secs = divmod(secs, 60)
        return f"{hrs} hours, {mins} minutes, {secs} seconds"

    def show_active_time(self):
        total_time_str = self.format_time(self.active_time)
        deck_times_str = "\n".join([f"Deck {mw.col.decks.name(did)}: {self.format_time(time)}" for did, time in self.deck_times.items()])
        note_type_times_str = "\n".join([f"Note Type {mw.col.models.name(nid)}: {self.format_time(time)}" for nid, time in self.note_type_times.items()])
        profile_times_str = "\n".join([f"Profile {profile}: {self.format_time(time)}" for profile, time in self.profile_times.items()])
        showInfo(f"Active Time: {total_time_str}\n\nDeck Times:\n{deck_times_str}\n\nNote Type Times:\n{note_type_times_str}\n\nProfile Times:\n{profile_times_str}")

# Đoạn mã này không thay đổi, chỉ để đảm bảo rằng dữ liệu được tải đúng cách
def load_sessions(self):
    if os.path.exists(self.session_file):
        with open(self.session_file, 'r') as f:
            self.sessions = json.load(f)
        # Cập nhật các phiên làm việc hiện tại để đảm bảo 'studied_cards' tồn tại
        for session in self.sessions:
            if 'studied_cards' not in session:
                session['studied_cards'] = 0
    else:
        self.sessions = []
