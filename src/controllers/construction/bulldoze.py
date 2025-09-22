
from services.bulldoze import BulldozeTargetType
from models.construction import ConstructionState
from models.map import RailMap
from services.bulldoze import get_bulldoze_target

def handle_bulldoze_click(state: ConstructionState, map: RailMap, pos: tuple[int, int], camera_scale):
    target = get_bulldoze_target(map, pos, camera_scale)

    if target.type == BulldozeTargetType.STATION:
        map.remove_station(target.data)
    elif target.type == BulldozeTargetType.SIGNAL:
        map.remove_signal_at(target.data)
    elif target.type == BulldozeTargetType.NODE or target.type == BulldozeTargetType.EDGE:
        map.remove_segment_at(target.data)