from enum import Enum

class ViewMode(Enum):
    NORMAL = 0
    CONSTRUCTION = 1
    
    
class AppState:
    mode: ViewMode = ViewMode.CONSTRUCTION