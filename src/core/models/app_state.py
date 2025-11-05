from enum import Enum
from typing import Callable, Optional

class ViewMode(Enum):
    SIMULATION = 0
    CONSTRUCTION = 1
    
class AppState:
    def __init__(self) -> None:
        self._mode: ViewMode = ViewMode.CONSTRUCTION
        self.callback: Optional[Callable[[ViewMode], None]] = None
    
    def subscribe(self, callback: Callable[[ViewMode], None]) -> None:
        self.callback = callback

    @property
    def mode(self) -> ViewMode:
        return self._mode

    @mode.setter
    def mode(self, value: ViewMode) -> None:
        self._mode = value
        if self.callback is not None:
            self.callback(value)