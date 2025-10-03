from models.map import RailMap
from models.construction import ConstructionState
from models.geometry import Position, Pose

def handle_rail_click(map: RailMap, pos: Position, state: ConstructionState):
    snapped = pos.snap_to_grid()
    if map.is_blocked(snapped):
        return
    if state.construction_anchor is None:
        state.construction_anchor = Pose(snapped, (0,0))
    elif snapped == state.construction_anchor.position:
        state.construction_anchor = None
    else:
        found_path = map.find_path(state.construction_anchor, snapped)
        if not found_path:
            return
        map.add_segment(found_path)
        state.construction_anchor = Pose(snapped, found_path[-2].direction_to(snapped))

