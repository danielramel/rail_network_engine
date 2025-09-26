from models.map import RailMap, find_path
from models.construction import ConstructionState
from models.position import Position, PositionWithDirection

def handle_rail_click(state: ConstructionState, map: RailMap, pos: Position):
    snapped = pos.snap_to_grid()
    if state.construction_anchor is None:
        state.construction_anchor = PositionWithDirection(snapped, (0,0))
    elif snapped == state.construction_anchor.position:
        state.construction_anchor = None
    else:
        found_path = find_path(state.construction_anchor, snapped)
        map.add_segment(found_path)
        state.construction_anchor = PositionWithDirection(snapped, found_path[-2].direction_to(snapped))

