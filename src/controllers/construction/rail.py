from utils import get_direction_between_points, snap_to_grid
from models.map import RailMap, find_path
from models.construction import ConstructionState
from models.geometry import PointWithDirection

def handle_rail_click(state: ConstructionState, network: RailMap, pos: tuple[int, int]):
    snapped = snap_to_grid(*pos)
    if state.construction_anchor is None:
        state.construction_anchor = PointWithDirection(snapped, (0,0))
    elif snapped == state.construction_anchor.point:
        state.construction_anchor = None
    else:
        found_path = find_path(state.construction_anchor, snapped)
        
        network.add_segment(
            network.add_node(found_path[0]),
            network.add_node(found_path[-1]),
            found_path
        )
        state.construction_anchor = PointWithDirection(snapped, get_direction_between_points(found_path[-2], snapped))

