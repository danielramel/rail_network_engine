from domain.rail_map import RailMap
from models.construction import ConstructionState
from models.geometry import Position, Pose
from services.construction.rail_target import find_rail_target

def handle_rail_click(map: RailMap, world_pos: Position, state: ConstructionState):
    target = find_rail_target(map, world_pos, state.construction_anchor)

    if target.kind == 'blocked':
        return

    if target.kind == 'node':
        state.construction_anchor = Pose(target.snapped, (0, 0))
        return

    if target.kind == 'anchor_same':
        state.construction_anchor = None
        return

    if target.kind == 'no_path':
        return

    if target.kind == 'path':
        map.add_segment(target.found_path, state.track_speed)
        state.construction_anchor = Pose(target.snapped, target.found_path[-2].direction_to(target.snapped))
        return
