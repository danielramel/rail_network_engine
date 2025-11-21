from dataclasses import dataclass
from enum import Enum, auto
from core.models.geometry import Edge
from core.models.time import Time
from core.models.train import TrainConfig

class SetupTool(Enum):
    PLACE_TRAIN = auto()
    REMOVE_TRAIN = auto()

class SetupAction(Enum):
    ADD = auto()
    REMOVE = auto()

@dataclass
class SetupPreview:
    edge: Edge | None = None
    action: SetupAction | None = None
    
    
    def clear(self) -> None:
        self.edge = None
        self.action = None
        

class SetupState:
    preview: SetupPreview
    tool: SetupTool
    time: Time
    train_config: TrainConfig
    
    def __init__(self, time: Time) -> None:
        self.preview = SetupPreview()
        self.tool = SetupTool.PLACE_TRAIN
        self.time = time
        self.train_config = TrainConfig()
    
    def switch_tool(self, new_tool: SetupTool) -> None:
        """Switch to a new setup tool, clearing previous state."""
        if new_tool == self.tool:
            return
        self.tool = new_tool
        self.preview.clear()