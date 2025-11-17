from dataclasses import dataclass, field
from core.models.geometry.edge import Edge
from core.models.geometry.position import Position
from core.models.signal import Signal
from core.models.train import Train
from enum import Enum
from core.config.settings import FPS
from core.models.time import Time

class TimeControlMode(Enum):
    PAUSE = 0
    PLAY = 1
    FAST_FORWARD = 3
    SUPER_FAST_FORWARD = 10
    

class TimeControlState:
    mode: TimeControlMode = TimeControlMode.PAUSE    
    def reset(self) -> None:
        """Reset the time control state to its initial values."""
        self.mode = TimeControlMode.PAUSE
        self.time = Time(0)
        
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
    train_id: int = None
    
    def clear(self) -> None:
        self.path = []
        self.signal = None
        self.train_id = None
        
@dataclass
class SimulationState:
    time: Time
    selected_signal: Signal = None
    time_control: TimeControlState = TimeControlState()
    preview: SimulationPreview = field(default_factory=SimulationPreview)
    _selected_trains: list[int] = field(default_factory=list)
    selected_trains_callback: callable = None
    
    def tick(self) -> None:
        """Advance the current time by the specified number of seconds."""
        self.time.add(1 * self.time_control.mode.value / FPS)
        

    
    def select_train(self, train_id: int) -> None:
        if train_id not in self._selected_trains:
            self._selected_trains.append(train_id)
        if self.selected_trains_callback:
            self.selected_trains_callback(train_id, True)
            
    def deselect_train(self, train_id: int) -> None:
        if train_id in self._selected_trains:
            self._selected_trains.remove(train_id)
        if self.selected_trains_callback:
            self.selected_trains_callback(train_id, False)