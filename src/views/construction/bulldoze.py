from pygame import Surface
from config.colors import RED, WHITE
from models.geometry import Position
from services.construction.bulldoze import CursorTarget, get_bulldoze_target
from ui_elements.draw_utils import draw_node, draw_signal, draw_station, draw_edges
from graphics.camera import Camera
from models.map import RailMap

def render_bulldoze_preview(surface: Surface, world_pos: Position, map: RailMap, camera: Camera):
    target = get_bulldoze_target(map, world_pos, camera.scale)
    
    if target.type == CursorTarget.EMPTY:
        draw_node(surface, target.data, camera, color=RED)
    elif target.type == CursorTarget.STATION:
        station = map.get_station_at(target.data)
        draw_station(surface, station, camera, color=RED)
    elif target.type == CursorTarget.SIGNAL:
        signal = map.get_signal_at(target.data)
        draw_signal(surface, signal, camera, color=RED)
    elif target.type == CursorTarget.PLATFORM:
        _, edges = map.get_segment(target.data)
        draw_edges(surface, edges, camera, color=WHITE)
    elif target.type == CursorTarget.EDGE:
        _, edges = map.get_segment(target.data)
        draw_edges(surface, edges, camera, color=RED)