import pygame
from config.colors import RED
from models.geometry import PointWithDirection
from services.bulldoze import BulldozeTargetType, get_bulldoze_target
from ui_elements.draw_utils import draw_node, draw_signal, draw_station
from utils import point_within_station_rect, snap_to_grid, point_line_intersection, is_point_near_grid
from graphics.camera import Camera
from models.map import RailMap
from models.construction import ConstructionState

def render_bulldoze_preview(surface : pygame.Surface, camera: Camera, state: ConstructionState, map: RailMap, pos: tuple[int, int]):
    world_pos = camera.screen_to_world(*pos)
    target = get_bulldoze_target(map, world_pos, camera.scale)
    

    if target.type == BulldozeTargetType.EMPTY:
        draw_node(surface, camera, snap_to_grid(*world_pos), color=RED)
    elif target.type == BulldozeTargetType.STATION:
        draw_station(surface, camera, target.data, map.stations[target.data], color=RED)
    elif target.type == BulldozeTargetType.SIGNAL:
        draw_signal(surface, camera, PointWithDirection(point=target.data, direction=map.graph.nodes[target.data]['signal']), color=RED)
    elif target.type == BulldozeTargetType.EDGE:
        _, edges = map.get_segments_at(target.data)
        for edge in edges:
            screen_points = [tuple(camera.world_to_screen(p.x, p.y)) for p in edge]
            pygame.draw.line(surface, RED, *screen_points, max(1, int(8 * camera.scale)))
    elif target.type == BulldozeTargetType.NODE:
        nodes, edges = map.get_segments_at(target.data)
        
        for edge in edges:
            screen_points = [tuple(camera.world_to_screen(p.x, p.y)) for p in edge]
            pygame.draw.line(surface, RED, *screen_points, max(1, int(8 * camera.scale)))
        for node in nodes:
            if map.graph.degree[node] > 2:
                draw_node(surface, camera, node, color=RED)