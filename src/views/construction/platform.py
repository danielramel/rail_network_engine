from pygame import Surface
from config.colors import PURPLE, RED
from config.settings import MINIMUM_PLATFORM_LENGTH
from graphics.camera import Camera
from models.map import RailMap
from models.construction import CursorTarget
from ui_elements.draw_utils import draw_dashed_line, draw_edges, draw_node, draw_station
from services.construction.platform import get_platform_context
from models.geometry import Position
    

def render_platform_preview(surface: Surface, world_pos: Position, map: RailMap, camera: Camera):
    context = get_platform_context(map, world_pos, camera.scale)
    if context.type == CursorTarget.EDGE:
        _, edges = map.get_segments_at(context.data, end_on_signal=False)  # can change end_on_signal to True if desired
        color = RED if len(edges) < MINIMUM_PLATFORM_LENGTH else PURPLE
        draw_edges(surface, edges, camera, color=color)
    elif context.type == CursorTarget.EMPTY:
        draw_node(surface, camera, context.data, color=PURPLE)

    if context.nearest_station is not None and context.type != CursorTarget.NODE:
        draw_station(surface, camera, context.nearest_station, map.get_all_stations()[context.nearest_station].name, color=PURPLE)
        start = camera.world_to_screen(context.nearest_station)
        if context.type == CursorTarget.EDGE:
            end = camera.world_to_screen(Position.midpoint(*context.data))
        else:
            end = camera.world_to_screen(context.data)
        draw_dashed_line(surface, start, end, PURPLE)