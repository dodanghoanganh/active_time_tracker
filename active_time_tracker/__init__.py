from aqt import mw
from aqt.qt import QAction
from .ui.main_window import MainWindow
from .utils.active_time_tracker import ActiveTimeTracker

tracker = ActiveTimeTracker()

def main():
    action = QAction("Active Time Tracker", mw)
    action.triggered.connect(open_main_window)
    mw.form.menuTools.addAction(action)
    
    show_time_action = QAction("Show Active Time", mw)
    show_time_action.triggered.connect(tracker.show_active_time)
    mw.form.menuTools.addAction(show_time_action)

def open_main_window():
    mw.active_time_tracker_window = MainWindow()
    mw.active_time_tracker_window.show()

main()
