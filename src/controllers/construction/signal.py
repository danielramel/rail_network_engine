from models.geometry import Pose
from models.map import RailMap
from models.geometry import Position

def handle_signal_click(map: RailMap, pos: Position):
    snapped = pos.snap_to_grid()
    if not map.has_node_at(snapped):  # empty click
        return
    
    if map.is_junction(snapped): 
        return # intersection, no signals here
    
    if map.has_signal_at(snapped):
        if map.degree_at(snapped) == 1:
            return # dead end, cannot toggle
        map.toggle_signal_at(snapped)
        return
    
    map.add_signal_at(snapped)
    