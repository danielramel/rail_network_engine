from utils import snap_to_grid
from models.map import RailMap
from models.construction import ConstructionState

def handle_station_click(state: ConstructionState, network: RailMap, pos: tuple[int, int]):
    snapped = snap_to_grid(*pos)
    
    
    
    
