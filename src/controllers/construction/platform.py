from models.map import RailMap
from models.construction import CursorTarget
from services.construction.platform import get_platform_context
from models.geometry import Position
from config.settings import MINIMUM_PLATFORM_LENGTH
from ui_elements.alert import alert


def handle_platform_click(map: RailMap, pos: Position, camera_scale):
    context = get_platform_context(map, pos, camera_scale)
    if context.type == CursorTarget.EDGE:
        edges, _ = context.data
        if len(edges) < MINIMUM_PLATFORM_LENGTH:
            alert(f'Platform too short! Minimum length is {MINIMUM_PLATFORM_LENGTH} segments.')
            return
        
        map.add_platform_on(edges, context.station)
        