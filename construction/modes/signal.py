from utils import snap_to_grid, get_direction_between_points
from graphics.camera import Camera
from network import RailNetwork
from construction.models import ConstructionState
from network import PointWithDirection

def handle_signal_click(state: ConstructionState, camera: Camera, network: RailNetwork, pos):
    snapped = snap_to_grid(*camera.screen_to_world(*pos))
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
    