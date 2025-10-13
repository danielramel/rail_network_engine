from enum import Enum

class ViewMode(Enum):
    SIMULATION = 0
    CONSTRUCTION = 1
    TIMETABLE = 2
    
    
class AppState:
    mode: ViewMode = ViewMode.CONSTRUCTION