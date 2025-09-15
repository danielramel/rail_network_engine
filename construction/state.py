# construction/state.py
from dataclasses import dataclass, field
from models import PointWithDirection
from .ui_helpers import ConstructionMode

@dataclass
class ConstructionState:
    Mode: ConstructionMode = ConstructionMode.RAIL
    construction_anchor: PointWithDirection | None = None
