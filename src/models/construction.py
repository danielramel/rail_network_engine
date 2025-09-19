# construction/models.py
from dataclasses import dataclass
from enum import Enum
from models.geometry import PointWithDirection

class ConstructionMode(Enum):
    RAIL = 1
    SIGNAL = 2
    STATION = 3
    BULLDOZE = 4
    
@dataclass
class ConstructionState:
    Mode: ConstructionMode = ConstructionMode.RAIL
    construction_anchor: PointWithDirection | None = None

