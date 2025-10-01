from models.geometry import Position
from services.construction.bulldoze import CursorTarget
from models.map import RailMap
from services.construction.bulldoze import get_bulldoze_target

def handle_bulldoze_click(map: RailMap, pos: Position, camera_scale):
    target = get_bulldoze_target(map, pos, camera_scale)

    if target.type == CursorTarget.SIGNAL:
        map.remove_signal_at(target.data)
    elif target.type == CursorTarget.STATION:
        map.remove_station_at(target.data)
    elif target.type == CursorTarget.PLATFORM:
        map.remove_platform_at(target.data)
    elif target.type == CursorTarget.EDGE:
        map.remove_segment_at(target.data)