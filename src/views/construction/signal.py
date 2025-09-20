import pygame
from models.geometry import PointWithDirection
from ui_elements.draw_utils import draw_signal
from utils import get_direction_between_points, snap_to_grid
from config.colors import GRAY, RED, YELLOW
from graphics.camera import Camera
from models.map import RailMap
from models.construction import ConstructionState


def render_signal_construction(surface : pygame.Surface, camera: Camera, state: ConstructionState, map: RailMap, pos: tuple[int, int]):
    snapped = snap_to_grid(*camera.screen_to_world(*pos))
    
    if snapped not in map.graph or map.graph.degree[snapped] > 2:
        signal_preview = PointWithDirection(point=snapped, direction=(-1, 0))
        draw_signal(surface, camera, signal_preview, color=RED, offset=True)

    else:
        if 'signal' in map.graph.nodes[snapped]:
            if len(map.graph[snapped]) == 1:
                signal_preview = PointWithDirection(point=snapped, direction=map.graph.nodes[snapped]['signal'])
                draw_signal(surface, camera, signal_preview, color=YELLOW, offset=True)
                return # dead end, cannot toggle
            
            current_direction = map.graph.nodes[snapped]['signal']
            neighbors = tuple(map.graph.neighbors(snapped))
            if get_direction_between_points(snapped, neighbors[0]) == current_direction:
                signal_preview = PointWithDirection(point=snapped, direction=get_direction_between_points(snapped, neighbors[1]))
            else:
                signal_preview = PointWithDirection(point=snapped, direction=get_direction_between_points(snapped, neighbors[0]))
                
            draw_signal(surface, camera, signal_preview, color=YELLOW, offset=True)
        else:
            signal_preview = PointWithDirection(point=snapped, direction=get_direction_between_points(snapped, next(map.graph.neighbors(snapped))))
            draw_signal(surface, camera, signal_preview, color=YELLOW)
