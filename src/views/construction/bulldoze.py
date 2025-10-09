import pygame
from config.colors import RED
from models.construction import ConstructionState
from models.geometry import Position
from ui.utils import draw_node, draw_signal, draw_station
from graphics.camera import Camera
from domain.rail_map import RailMap
from services.construction.bulldoze_target import find_bulldoze_target

def render_bulldoze_preview(surface: pygame.Surface, world_pos: Position, state: ConstructionState, map: RailMap, camera: Camera):
    target = find_bulldoze_target(map, world_pos, camera.scale)
    state.preview_edges = set()
    state.preview_nodes = set()
    state.preview_edges_type = None

    if target.kind == 'signal':
        draw_signal(surface, map.get_signal_at(target.pos), camera, color=RED)
    elif target.kind == 'station':
        draw_station(surface, map.get_station_at(target.pos), camera, color=RED)
    elif target.kind == 'node':
        draw_node(surface, world_pos, camera, color=RED)
    elif target.kind == 'platform':
        state.preview_edges = target.edges
        state.preview_edges_type = 'normal'
    elif target.kind == 'segment':
        state.preview_edges = target.edges
        state.preview_nodes = target.nodes
        state.preview_edges_type = 'bulldoze'
