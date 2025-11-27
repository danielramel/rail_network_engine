from enum import Enum, auto

class SetupView(Enum):
    CONSTRUCTION = auto()
    TRAIN_PLACEMENT = auto()
    
class SetupState:
    current_view: SetupView = SetupView.CONSTRUCTION
    _subscribers: list = []
    
    def switch_to(self, new_view: SetupView):
        self.current_view = new_view
        for callback in self._subscribers:
            callback(new_view)
    
    def subscribe(self, callback):
        self._subscribers.append(callback)