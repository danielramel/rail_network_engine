from utils import snap_to_grid
from models.map import RailMap
from models.construction import ConstructionState
from ui_elements.text_input import user_input
from utils import station_rects_overlap

def handle_station_click(state: ConstructionState, map: RailMap, pos: tuple[int, int]):
    snapped = snap_to_grid(*pos)
    
    inp = user_input()
    
    if inp in map.stations.values():
        return # Station name must be unique

    for station_pos in map.stations.keys():
        if station_rects_overlap(station_pos, snapped):
            return
        
    map.add_station_at(snapped, inp)