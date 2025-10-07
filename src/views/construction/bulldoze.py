import pygame
from config.colors import RED
from models.geometry import Position
from ui.utils import draw_node, draw_signal, draw_station
from graphics.camera import Camera
from domain.rail_map import RailMap
from services.construction.bulldoze_target import find_bulldoze_target

def render_bulldoze_preview(surface: pygame.Surface, world_pos: Position, mode_info: dict, map: RailMap, camera: Camera):
    target = find_bulldoze_target(map, world_pos, camera.scale)
    mode_info['preview_edges'] = set()
    mode_info['preview_nodes'] = set()
    mode_info['edge_type'] = None

    if target.kind == 'signal':
        draw_signal(surface, map.get_signal_at(target.pos), camera, color=RED)
    elif target.kind == 'station':
        draw_station(surface, map.get_station_at(target.pos), camera, color=RED)
    elif target.kind == 'node':
        draw_node(surface, world_pos, camera, color=RED)
    elif target.kind == 'platform':
        mode_info['preview_edges'] = target.edges
        mode_info['edge_type']='normal'
    elif target.kind == 'segment':
        mode_info['preview_edges'] = target.edges
        mode_info['edge_type']='red'
        mode_info['preview_nodes'] = target.nodes
