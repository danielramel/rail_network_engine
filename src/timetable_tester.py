from models.simulation import Simulation
from models.geometry.position import Position

from views.timetable.timetable_view import TimetableWindow
from PyQt6.QtWidgets import QApplication
import sys

simulation = Simulation()
simulation.stations.add(Position(0, 0), "Station A")
simulation.stations.add(Position(100, 0), "Station B")
simulation.stations.add(Position(200, 0), "Station C")
simulation.stations.add(Position(300, 0), "Station D")

qt_app = QApplication.instance() or QApplication(sys.argv)

if __name__ == "__main__":
    main_win = TimetableWindow(simulation)  # keep a reference
    main_win.show()
    sys.exit(qt_app.exec())  # run the Qt event loop
