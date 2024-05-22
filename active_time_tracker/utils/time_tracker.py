import time
import json
import os
from datetime import datetime
from .active_time_tracker import ActiveTimeTracker

class TimeTracker:
    def __init__(self, config_path=None):
        self.start_time = None
        self.total_active_time = 0
        self.idle_threshold = 60  # Default to 1 minute
        self.last_active_time = time.time()
        self.log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'time_logs.json')

        if config_path:
            with open(config_path, "r") as f:
                config = json.load(f)
            self.idle_threshold = config["idle_time"]

        self.active_tracker = ActiveTimeTracker()
        self.load_logs()

    def start_session(self):
        self.start_time = time.time()
        self.last_active_time = self.start_time

    def end_session(self):
        if self.start_time:
            active_time = time.time() - self.start_time
            self.total_active_time += active_time
            self.save_log(active_time)
            self.active_tracker.save_data()
            self.start_time = None

    def update_last_active_time(self):
        self.last_active_time = time.time()

    def get_total_active_time(self):
        return self.total_active_time

    def is_idle(self):
        return time.time() - self.last_active_time > self.idle_threshold

    def load_logs(self):
        try:
            with open(self.log_file, "r") as f:
                self.logs = json.load(f)
        except FileNotFoundError:
            self.logs = []

    def save_log(self, active_time):
        now = datetime.now()
        log_entry = {
            "date": now.strftime("%d-%m-%Y %H:%M:%S"),
            "active_time": active_time
        }
        self.logs.append(log_entry)
        with open(self.log_file, "w") as f:
            json.dump(self.logs, f, indent=4)

    def get_logs(self):
        return self.logs
