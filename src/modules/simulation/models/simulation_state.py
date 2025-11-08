from dataclasses import dataclass, field
from core.models.geometry.edge import Edge
from core.models.geometry.position import Position
from core.models.signal import Signal

from enum import Enum
from core.config.settings import FPS

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
    
    def switch_mode(self, mode: TimeControlMode) -> None:
        self.mode = mode
        
    def toggle_pause(self) -> None:
        self.mode = TimeControlMode.PLAY if self.paused else TimeControlMode.PAUSE
    
@dataclass
class SimulationPreview:
    path: list[Edge] = field(default_factory=list)
    signal: Position = None
    
    def clear(self) -> None:
        self.path = []
        self.signal = None

@dataclass
class SimulationState:
    selected_signal: Signal = None
    time: TimeControlState = TimeControlState()
    preview: SimulationPreview = field(default_factory=SimulationPreview)