from domain.rail_map import RailMap
from models.geometry import Position, Pose
from services.construction.rail_target import find_rail_target

def handle_rail_click(map: RailMap, pos: Position, mode_info: dict):
    construction_anchor: Pose = mode_info.get('construction_anchor')
    target = find_rail_target(map, pos, construction_anchor)

    if target.kind == 'blocked':
        return

    if target.kind == 'node':
        mode_info['construction_anchor'] = Pose(target.snapped, (0, 0))
        return

    if target.kind == 'anchor_same':
        mode_info['construction_anchor'] = None
        return

    if target.kind == 'no_path':
        return

    if target.kind == 'path':
        map.add_segment(target.found_path, mode_info['track_speed'])
        mode_info['construction_anchor'] = Pose(target.snapped, target.found_path[-2].direction_to(target.snapped))
        return
