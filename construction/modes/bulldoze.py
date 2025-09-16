from graphics.camera import Camera
from construction.models import ConstructionState
from network import RailNetwork
from utils import snap_to_grid

#todo: figure out how to delete edges too
def handle_bulldoze_click(state: ConstructionState, camera: Camera, network: RailNetwork, pos: tuple[int, int]):
    snapped = snap_to_grid(*camera.screen_to_world(*pos))
    if snapped not in network.graph: # empty click
        return
    if 'signal' in network.graph.nodes[snapped]:
        network.remove_signal_at(snapped)
        return
    network.remove_node_at(snapped)