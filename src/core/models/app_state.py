from enum import Enum, auto
from typing import Callable, Optional


class SimulationPhase(Enum):
    SETUP = auto()
    SIMULATION = auto()
    
class AppState:
    def __init__(self, filepath: Optional[str] = None) -> None:
        self._phase: SimulationPhase = SimulationPhase.SETUP
        self.filepath: Optional[str] = filepath
        self.callback: Optional[Callable[[SimulationPhase], None]] = None
    
    def subscribe(self, callback: Callable[[SimulationPhase], None]) -> None:
        self.callback = callback

    @property
    def phase(self) -> SimulationPhase:
        return self._phase
    
    def switch_phase(self, phase: SimulationPhase) -> None:
        if self._phase == phase:
            return
        self._phase = phase
        if self.callback is not None:
            self.callback(phase)