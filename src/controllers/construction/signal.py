from models.geometry import Pose
from models.map import RailMap
from models.geometry import Position

def handle_signal_click(map: RailMap, pos: Position):
    snapped = pos.snap_to_grid()
    if not map.has_node_at(snapped):  # empty click
        return
    
    if map.is_intersection(snapped): 
        return # intersection, no signals here
    
    if map.has_signal_at(snapped):
        if len(map.graph[snapped]) == 1:
            return # dead end, cannot toggle
        map.toggle_signal_at(snapped)
        return

    direction = snapped.direction_to(next(map.graph.neighbors(snapped)))
    
    signal = Pose(position=snapped, direction=direction)
    
    map.add_signal_at(signal)
    