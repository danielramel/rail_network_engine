from pygame import Surface
from config.colors import RED, WHITE
from models.geometry import Position
from services.construction.bulldoze import CursorTarget, get_bulldoze_target
from ui.utils import draw_node, draw_signal, draw_station, draw_edges
from graphics.camera import Camera
from models.map import RailMap

def render_bulldoze_preview(surface: Surface, world_pos: Position, mode_info: dict, map: RailMap, camera: Camera):
    target = get_bulldoze_target(map, world_pos, camera.scale)
    
    mode_info['preview_edges'] = set()
    mode_info['preview_nodes'] = set()
    mode_info['preview_type'] = None
    if target.type == CursorTarget.EMPTY:
        draw_node(surface, target.data, camera, color=RED)
    elif target.type == CursorTarget.STATION:
        station = map.get_station_at(target.data)
        draw_station(surface, station, camera, color=RED)
    elif target.type == CursorTarget.SIGNAL:
        signal = map.get_signal_at(target.data)
        draw_signal(surface, signal, camera, color=RED)
    elif target.type == CursorTarget.EDGE:
        nodes, edges = map.get_segment(target.data)
        mode_info['preview_edges'].update(edges)
        mode_info['preview_nodes'].update(nodes)
        mode_info['preview_type'] = 'bulldoze'
    elif target.type == CursorTarget.PLATFORM:
        _, edges = map.get_segment(target.data)
        draw_edges(surface, edges, camera, color=WHITE)
    