from dataclasses import dataclass, field
from core.models.geometry.edge import Edge
from core.models.signal import Signal
from typing import Callable, Optional
from enum import Enum
from core.config.config import Config
from core.models.time import Time

class TimeControlMode(Enum):
    PAUSE = 0
    PLAY = 1
    FAST_FORWARD = 5
    SUPER_FAST_FORWARD = 30
    

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
    signal: Optional[Signal] = None
    automatic_signal: bool = False
    train_id: Optional[int] = None
    
    def clear(self) -> None:
        self.path = []
        self.signal = None
        self.train_id = None
        self.automatic_signal = False
        
@dataclass
class SimulationState:
    time: Time
    selected_signal: Optional[Signal] = None
    time_control: TimeControlState = field(default_factory=TimeControlState)
    preview: SimulationPreview = field(default_factory=SimulationPreview)
    selected_trains: set[int] = field(default_factory=set)
    _selected_train: Optional[int] = None
    _train_selected_callback: Optional[Callable] = None
    _train_deselected_callback: Optional[Callable] = None
    
    def tick(self) -> None:
        """Advance the current time by the specified number of seconds."""
        self.time.add(1 * self.time_control.mode.value / Config.FPS)
        
    def select_train(self, train_id: int) -> None:
        if train_id not in self.selected_trains:
            self.selected_trains.add(train_id)
        self._selected_train = train_id
        if self._train_selected_callback:
            self._train_selected_callback(train_id)
            
    def deselect_train(self, train_id: int) -> None:
        if self._selected_train == train_id:
            self._selected_train = None
        self.selected_trains.remove(train_id)
        if self._train_deselected_callback:
            self._train_deselected_callback(train_id)
            
    def subscribe_to_train_selected(self, callback: Callable) -> None:
        self._train_selected_callback = callback
        
    def subscribe_to_train_deselected(self, callback: Callable) -> None:
        self._train_deselected_callback = callback