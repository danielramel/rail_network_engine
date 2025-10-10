from enum import Enum
from models.geometry import Position
from dataclasses import dataclass

class CLICK_TYPE(Enum):
    LEFT_CLICK = 0
    RIGHT_CLICK = 1
    
@dataclass
class Event:
    click_type: CLICK_TYPE
    screen_pos: Position