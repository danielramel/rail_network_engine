import pygame
from models.position import Position, PositionWithDirection
from ui_elements.draw_utils import draw_signal
from config.colors import GRAY, RED, YELLOW
from graphics.camera import Camera
from models.map import RailMap
from models.construction import ConstructionState


def render_signal_preview(surface : pygame.Surface, camera: Camera, state: ConstructionState, map: RailMap, pos: Position):
    snapped = camera.screen_to_world(pos).snap_to_grid()

    if snapped not in map.graph or map.graph.degree[snapped] > 2:
        signal_preview = PositionWithDirection(position=snapped, direction=(-1, 0))
        draw_signal(surface, camera, signal_preview, color=RED, offset=True)

    else:
        if 'signal' in map.graph.nodes[snapped]:
            if len(map.graph[snapped]) == 1:
                signal_preview = PositionWithDirection(position=snapped, direction=map.graph.nodes[snapped]['signal'])
                draw_signal(surface, camera, signal_preview, color=YELLOW, offset=True)
                return # dead end, cannot toggle
            
            current_direction = map.graph.nodes[snapped]['signal']
            neighbors = tuple(map.graph.neighbors(snapped))
            if snapped.direction_to(neighbors[0]) == current_direction:
                signal_preview = PositionWithDirection(position=snapped, direction=snapped.direction_to(neighbors[1]))
            else:
                signal_preview = PositionWithDirection(position=snapped, direction=snapped.direction_to(neighbors[0]))

            draw_signal(surface, camera, signal_preview, color=YELLOW, offset=True)
        else:
            signal_preview = PositionWithDirection(position=snapped, direction=snapped.direction_to(next(map.graph.neighbors(snapped))))
            draw_signal(surface, camera, signal_preview, color=YELLOW)
