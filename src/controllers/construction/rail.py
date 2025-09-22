from utils import get_direction_between_points, snap_to_grid
from models.map import RailMap, find_path
from models.construction import ConstructionState
from models.geometry import PointWithDirection

def handle_rail_click(state: ConstructionState, map: RailMap, pos: tuple[int, int]):
    snapped = snap_to_grid(*pos)
    if state.construction_anchor is None:
        state.construction_anchor = PointWithDirection(snapped, (0,0))
    elif snapped == state.construction_anchor.point:
        state.construction_anchor = None
    else:
        found_path = find_path(state.construction_anchor, snapped)
        map.add_segment(found_path)
        state.construction_anchor = PointWithDirection(snapped, get_direction_between_points(found_path[-2], snapped))

