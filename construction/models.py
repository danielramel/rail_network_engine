# construction/models.py
from dataclasses import dataclass
from enum import Enum
from models import PointWithDirection

class ConstructionMode(Enum):
    RAIL = 'R'
    LIGHT = 'L'
    PLATFORM = 'P'
    STATION = 'S'
    BULLDOZE = 'B'
    
@dataclass
class ConstructionState:
    Mode: ConstructionMode = ConstructionMode.RAIL
    construction_anchor: PointWithDirection | None = None

