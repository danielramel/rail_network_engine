from models.position import PositionWithDirection
from models.map import RailMap
from models.construction import ConstructionState
from models.position import Position

def handle_signal_click(state: ConstructionState, map: RailMap, pos: Position):
    snapped = pos.snap_to_grid()
    if snapped not in map.graph: # empty click
        return
    
    if map.graph.degree[snapped] > 2: 
        return # intersection, no signals here
    
    if map.has_signal_at(snapped):
        if len(map.graph[snapped]) == 1:
            return # dead end, cannot toggle
        map.toggle_signal_at(snapped)
        return

    direction = snapped.direction_to(next(map.graph.neighbors(snapped)))
    
    signal = PositionWithDirection(position=snapped, direction=direction)
    
    map.add_signal_at(signal)
    