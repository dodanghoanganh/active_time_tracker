import json
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        with open("active_time_tracker/config.json", "r") as f:
            self.config = json.load(f)

    def generate_report(self, active_time):
        now = datetime.now()
        report = {
            "date": now.strftime("%d-%m-%Y"),
            "active_time": active_time
        }
        return report

    def save_report(self, report):
        report_file = f"report_{report['date']}.json"
        with open(f"active_time_tracker/reports/{report_file}", "w") as f:
            json.dump(report, f)
