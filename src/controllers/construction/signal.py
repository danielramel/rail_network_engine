from utils import snap_to_grid, get_direction_between_points
from models.geometry import PointWithDirection
from models.map import RailMap
from models.construction import ConstructionState

def handle_signal_click(state: ConstructionState, network: RailMap, pos: tuple[int, int]):
    snapped = snap_to_grid(*pos)
    if snapped not in network.graph: # empty click
        return
    
    if network.graph.degree[snapped] > 2: 
        return # intersection, no signals here
    
    if 'signal' in network.graph.nodes[snapped]:
        if len(network.graph[snapped]) == 1:
            return # dead end, cannot toggle
        network.toggle_signal_at(snapped)
        return

    direction = get_direction_between_points(snapped, next(network.graph.neighbors(snapped)))
    
    signal = PointWithDirection(point=snapped, direction=direction)
    
    network.add_signal_at(signal)
    