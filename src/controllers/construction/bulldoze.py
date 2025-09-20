from utils import snap_to_grid
from models.construction import ConstructionState
from models.map import RailMap

#todo: figure out how to delete edges too
def handle_bulldoze_click(state: ConstructionState, map: RailMap, pos: tuple[int, int]):
    snapped = snap_to_grid(*pos)
    if snapped not in map.graph: # empty click
        return
    if 'signal' in map.graph.nodes[snapped]:
        map.remove_signal_at(snapped)
        return
    map.remove_node_at(snapped)