# construction/models.py
from dataclasses import dataclass
from enum import Enum
from models.geometry import PointWithDirection

class ConstructionMode(Enum):
    RAIL = 'R'
    SIGNAL = 'S'
    STATION = 'S'
    BULLDOZE = 'B'
    
@dataclass
class ConstructionState:
    Mode: ConstructionMode = ConstructionMode.RAIL
    construction_anchor: PointWithDirection | None = None

