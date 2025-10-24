from models.railway_system import RailwaySystem
from models.geometry.position import Position

from views.timetable.timetable_view import TimetableWindow
from PyQt6.QtWidgets import QApplication
import sys

railway = RailwaySystem()
railway.stations.add(Position(0, 0), "Station A")
railway.stations.add(Position(100, 0), "Station B")
railway.stations.add(Position(200, 0), "Station C")
railway.stations.add(Position(300, 0), "Station D")

qt_app = QApplication.instance() or QApplication(sys.argv)

if __name__ == "__main__":
    main_win = TimetableWindow(railway)  # keep a reference
    main_win.show()
    sys.exit(qt_app.exec())  # run the Qt event loop
