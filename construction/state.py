# construction/state.py
from dataclasses import dataclass, field
from typing import List
from rail_network import Point
from .ui_helpers import ConstructionMode

@dataclass
class ConstructionState:
    selected_mode: ConstructionMode = ConstructionMode.RAIL
    rail_construction_points: List[Point] = field(default_factory=list)
