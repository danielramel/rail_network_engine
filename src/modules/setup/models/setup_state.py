from dataclasses import dataclass, field
from enum import Enum, auto
from core.models.geometry import Edge

class SetupMode(Enum):
    PLACE_TRAIN = auto()
    REMOVE_TRAIN = auto()

@dataclass
class SetupPreview:
    edge: Edge | None = None
    reversed: bool = False
    
    def clear(self) -> None:
        self.edge = None
        self.reversed = False

@dataclass
class SetupState:
    preview: SetupPreview = field(default_factory=SetupPreview)
    mode: SetupMode = SetupMode.PLACE_TRAIN
    
    def switch_mode(self, new_mode: SetupMode) -> None:
        self.mode = new_mode