from utils import snap_to_grid, get_direction_between_points
from models.geometry import PointWithDirection
from models.map import RailMap
from models.construction import ConstructionState

def handle_signal_click(state: ConstructionState, map: RailMap, pos: tuple[int, int]):
    snapped = snap_to_grid(*pos)
    if snapped not in map.graph: # empty click
        return
    
    if map.graph.degree[snapped] > 2: 
        return # intersection, no signals here
    
    if 'signal' in map.graph.nodes[snapped]:
        if len(map.graph[snapped]) == 1:
            return # dead end, cannot toggle
        map.toggle_signal_at(snapped)
        return

    direction = get_direction_between_points(snapped, next(map.graph.neighbors(snapped)))
    
    signal = PointWithDirection(point=snapped, direction=direction)
    
    map.add_signal_at(signal)
    