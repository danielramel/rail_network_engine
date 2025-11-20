from enum import Enum, auto
from typing import Callable, Optional

from core.models.time import Time
from shared.ui.utils.popups import alert

class ViewMode(Enum):
    SETUP = auto()
    CONSTRUCTION = auto()
    SIMULATION = auto()
    
class AppState:
    def __init__(self, filename: Optional[str] = None) -> None:
        self._mode: ViewMode = ViewMode.SETUP
        self.filename: Optional[str] = filename
        self.callback: Optional[Callable[[ViewMode], None]] = None
        self.time = Time()
    
    def subscribe(self, callback: Callable[[ViewMode], None]) -> None:
        self.callback = callback

    @property
    def mode(self) -> ViewMode:
        return self._mode
    
    
    def switch_mode(self, new_mode: ViewMode) -> None:
        if self._mode == new_mode:
            return
        if new_mode == ViewMode.SIMULATION and self.time.current_time is None:
            alert("Cannot switch to SIMULATION mode: Time is not set.")
            return
        self._mode = new_mode
        if self.callback is not None:
            self.callback(new_mode)