from models.map import RailMap
from models.construction import ConstructionState, CursorTarget
from services.platform import get_platform_context
from models.position import Position
from config.settings import MINIMUM_PLATFORM_LENGTH


def handle_platform_click(state: ConstructionState, map: RailMap, pos: Position, camera_scale):
    context = get_platform_context(map, pos, camera_scale)
    if context.type == CursorTarget.EDGE:
        nodes, edges = map.get_segments_at(context.data, endOnSignal=False) # can change endOnSignal to True if desired
        if len(edges) >= MINIMUM_PLATFORM_LENGTH:   
            map.add_platform(nodes, edges, context.nearest_station)