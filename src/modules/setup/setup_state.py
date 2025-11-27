from enum import Enum, auto
from core.models.app_state import AppState

class SetupView(Enum):
    CONSTRUCTION = auto()
    TRAIN_PLACEMENT = auto()
    
class SetupState:
    current_view: SetupView = SetupView.CONSTRUCTION
    _subscribers: list = []
    _app_state: AppState
    
    def __init__(self, app_state: AppState):
        self._app_state = app_state
    
    def switch_to(self, new_view: SetupView):
        self.current_view = new_view
        for callback in self._subscribers:
            callback(new_view)
    
    def subscribe(self, callback):
        self._subscribers.append(callback)