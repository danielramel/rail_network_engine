from models.map import RailMap, find_path
from models.construction import ConstructionState
from models.map.pathfinding import can_be_part_of_path
from models.position import Position, Pose

def handle_rail_click(state: ConstructionState, map: RailMap, pos: Position):
    snapped = pos.snap_to_grid()
    if not can_be_part_of_path(snapped, map):
        return
    if state.construction_anchor is None:
        state.construction_anchor = Pose(snapped, (0,0))
    elif snapped == state.construction_anchor.position:
        state.construction_anchor = None
    else:
        found_path = find_path(state.construction_anchor, snapped, map)
        if not found_path:
            return
        map.add_segment(found_path)
        state.construction_anchor = Pose(snapped, found_path[-2].direction_to(snapped))

