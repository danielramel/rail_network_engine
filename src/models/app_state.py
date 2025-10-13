from enum import Enum

class ViewMode(Enum):
    SIMULATION = 0
    CONSTRUCTION = 1
    SCHEDULER = 2
    
    
class AppState:
    mode: ViewMode = ViewMode.CONSTRUCTION