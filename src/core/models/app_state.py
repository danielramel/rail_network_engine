from enum import Enum, auto
from typing import Callable, Optional


class AppPhase(Enum):
    SETUP = auto()
    SIMULATION = auto()
    
class AppState:
    def __init__(self, on_exit: Callable[[str], None], filepath: Optional[str]) -> None:
        self._phase: AppPhase = AppPhase.SETUP
        self.exit: Callable[[str], None] = on_exit
        self.filepath: Optional[str] = filepath
        self._switch_phase_callback: Optional[Callable[[AppPhase], None]] = None
    
    def subscribe(self, callback: Callable[[AppPhase], None]) -> None:
        self._switch_phase_callback = callback

    @property
    def phase(self) -> AppPhase:
        return self._phase
    
    def start_simulation(self) -> None:
        self.switch_phase(AppPhase.SIMULATION)
    
    def switch_phase(self, phase: AppPhase) -> None:
        if self._phase == phase:
            return
        self._phase = phase
        if self._switch_phase_callback is not None:
            self._switch_phase_callback(phase)