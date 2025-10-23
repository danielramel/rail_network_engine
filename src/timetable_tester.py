from domain.rail_map import RailMap
from models.geometry.position import Position

from views.timetable.timetable_view import TimetableWindow
from PyQt6.QtWidgets import QApplication
from models.schedule import TrainRepository
import sys

rmap = RailMap()
rmap.add_station_at(Position(0, 0), "Station A")
rmap.add_station_at(Position(100, 0), "Station B")
rmap.add_station_at(Position(200, 0), "Station C")
rmap.add_station_at(Position(300, 0), "Station D")

qt_app = QApplication.instance() or QApplication(sys.argv)

if __name__ == "__main__":
    repo = TrainRepository()
    main_win = TimetableWindow(repo, rmap)  # keep a reference
    main_win.show()
    sys.exit(qt_app.exec())  # run the Qt event loop
