from models.geometry import Position
from models.map import RailMap
from services.construction.bulldoze_target import BulldozeTarget, find_bulldoze_target

def handle_bulldoze_click(map: RailMap, world_pos: Position, camera_scale):
    target = find_bulldoze_target(map, world_pos, camera_scale)
    if target.kind == 'signal':
        map.remove_signal_at(target.pos)
    elif target.kind == 'station':
        map.remove_station_at(target.pos)
    elif target.kind == 'platform':
        map.remove_platform_at(target.edge)
    elif target.kind == 'segment':
        map.remove_segment_at(target.edge)
    # node/none -> nothing to do