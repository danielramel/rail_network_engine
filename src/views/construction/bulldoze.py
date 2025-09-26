import pygame
from config.colors import RED
from models.position import Position, PositionWithDirection
from services.bulldoze import CursorTarget, get_bulldoze_target
from ui_elements.draw_utils import draw_node, draw_signal, draw_station
from graphics.camera import Camera
from models.map import RailMap
from models.construction import ConstructionState

def render_bulldoze_preview(surface : pygame.Surface, camera: Camera, state: ConstructionState, map: RailMap, pos: Position):
    world_pos = camera.screen_to_world(pos)
    target = get_bulldoze_target(map, world_pos, camera.scale)
    

    if target.type == CursorTarget.EMPTY:
        draw_node(surface, camera, world_pos.snap_to_grid(), color=RED)
    elif target.type == CursorTarget.STATION:
        draw_station(surface, camera, target.data, map.stations[target.data], color=RED)
    elif target.type == CursorTarget.SIGNAL:
        draw_signal(surface, camera, PositionWithDirection(position=target.data, direction=map.graph.nodes[target.data]['signal']), color=RED)
    elif target.type == CursorTarget.EDGE:
        _, edges = map.get_segments_at(target.data)
        for edge in edges:
            screen_points = [tuple(camera.world_to_screen(Position(*p))) for p in edge]
            pygame.draw.aaline(surface, RED, *screen_points)
    elif target.type == CursorTarget.NODE:
        nodes, edges = map.get_segments_at(target.data)
        
        for edge in edges:
            screen_points = [tuple(camera.world_to_screen(Position(*p))) for p in edge]
            pygame.draw.aaline(surface, RED, *screen_points)
        for node in nodes:
            if map.graph.degree[node] > 2:
                draw_node(surface, camera, node, color=RED)
                
        draw_node(surface, camera, target.data, color=RED)