from dataclasses import dataclass
from enum import Enum, auto
from core.models.time import Time
from core.models.train import Train, TrainConfig

class TrainPlacementTool(Enum):
    PLACE_TRAIN = auto()
    REMOVE_TRAIN = auto()

@dataclass
class TrainPlacementPreview:
    train_id_to_remove: int | None = None
    train_to_preview: Train | None = None
    invalid_train_placement_edges: frozenset = frozenset()
    
    def clear(self) -> None:
        self.train_to_preview = None
        self.train_id_to_remove = None
        self.invalid_train_placement_edges = frozenset()

class TrainPlacementState:
    time: Time
    preview: TrainPlacementPreview = TrainPlacementPreview()
    tool: TrainPlacementTool = TrainPlacementTool.PLACE_TRAIN
    train_config: TrainConfig = TrainConfig()
    
    def __init__(self, time: Time) -> None:
        self.time = time
    
    def switch_tool(self, new_tool: TrainPlacementTool) -> None:
        """Switch to a new setup tool, clearing previous state."""
        if new_tool == self.tool:
            return
        self.tool = new_tool
        self.preview.clear()