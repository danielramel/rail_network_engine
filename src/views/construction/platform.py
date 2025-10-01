from pygame import Surface
from config.colors import LIGHTBLUE, RED
from config.settings import MINIMUM_PLATFORM_LENGTH
from graphics.camera import Camera
from models.map import RailMap
from models.construction import CursorTarget
from ui_elements.draw_utils import draw_dashed_line, draw_edges, draw_node, draw_station
from services.construction.platform import get_platform_context
from models.geometry import Position
    

def render_platform_preview(surface: Surface, world_pos: Position, map: RailMap, camera: Camera):
    context = get_platform_context(map, world_pos, camera.scale)
    
    start = context.station.position
    if context.type == CursorTarget.EMPTY:
        end = context.data
        draw_node(surface, context.data, camera, color=LIGHTBLUE)
        
    else:  # CursorTarget.EDGE
        edges, closest_edge = context.data
        end = world_pos.closest_point_to_edge(closest_edge)
        
        color = RED if len(edges) < MINIMUM_PLATFORM_LENGTH else LIGHTBLUE
        draw_edges(surface, edges, camera, color=color)


    draw_station(surface, context.station, camera, color=LIGHTBLUE)
    draw_dashed_line(surface, start, end, camera, LIGHTBLUE)