from dataclasses import dataclass, field
from enum import Enum, auto
from core.models.geometry import Edge

class SetupTool(Enum):
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
    tool: SetupTool = SetupTool.PLACE_TRAIN
    
    def switch_tool(self, new_tool: SetupTool) -> None:
        """Switch to a new setup tool, clearing previous state."""
        if new_tool == self.tool:
            return
        self.tool = new_tool
        self.preview.clear()