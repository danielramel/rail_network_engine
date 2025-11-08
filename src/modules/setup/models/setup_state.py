from dataclasses import dataclass, field
from core.models.geometry import Edge


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