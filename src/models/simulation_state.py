from dataclasses import dataclass
from models.signal import Signal

from enum import Enum
from config.settings import FPS

class TimeControlMode(Enum):
    PAUSE = 0
    PLAY = 1
    FAST_FORWARD = 3
    SUPER_FAST_FORWARD = 10
    
    
class TimeControlState:
    mode: TimeControlMode = TimeControlMode.PAUSE
    current_time = 0  # in seconds
    
    def reset(self) -> None:
        """Reset the time control state to its initial values."""
        self.mode = TimeControlMode.PAUSE
        self.current_time = 0
        
    def tick(self) -> None:
        """Advance the current time by the specified number of seconds."""
        self.current_time += 1 * self.mode.value / FPS
        
    @property
    def paused(self) -> bool:
        return self.mode == TimeControlMode.PAUSE

@dataclass
class SimulationState:
    selected_signal: Signal = None
    time: TimeControlState = TimeControlState()