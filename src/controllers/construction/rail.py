from models.map import RailMap
from models.geometry import Position, Pose

def handle_rail_click(map: RailMap, pos: Position, mode_info: dict):
    snapped = pos.snap_to_grid()
    construction_anchor: Pose = mode_info['construction_anchor']
    if map.is_blocked(snapped):
        return
    if not construction_anchor:
        mode_info['construction_anchor'] = Pose(snapped, (0,0))
    elif snapped == construction_anchor.position:
        mode_info['construction_anchor'] = None
    else:
        found_path = map.find_path(mode_info['construction_anchor'], snapped)
        if not found_path:
            return
        map.add_segment(found_path, mode_info['track_speed'])
        mode_info['construction_anchor'] = Pose(snapped, found_path[-2].direction_to(snapped))