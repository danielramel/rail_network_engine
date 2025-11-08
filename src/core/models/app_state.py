from enum import Enum
from typing import Callable, Optional

class ViewMode(Enum):
    SETUP = 0
    CONSTRUCTION = 1
    SIMULATION = 2
    
class AppState:
    def __init__(self) -> None:
        self._mode: ViewMode = ViewMode.CONSTRUCTION
        self.callback: Optional[Callable[[ViewMode], None]] = None
    
    def subscribe(self, callback: Callable[[ViewMode], None]) -> None:
        self.callback = callback

    @property
    def mode(self) -> ViewMode:
        return self._mode
    
    
    def switch_mode(self, new_mode: ViewMode) -> None:
        if self._mode == new_mode:
            return
        self._mode = new_mode
        if self.callback is not None:
            self.callback(new_mode)