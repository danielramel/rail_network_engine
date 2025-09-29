import pygame
from models.position import Position, PositionWithDirection
from ui_elements.draw_utils import draw_signal
from config.colors import GRAY, RED, YELLOW
from graphics.camera import Camera
from models.map import RailMap
from models.construction import ConstructionState


def render_signal_preview(surface : pygame.Surface, world_pos: Position, map: RailMap, camera: Camera):
    snapped = world_pos.snap_to_grid()

    if not map.has_node_at(snapped) or map.is_intersection(snapped):
        signal_preview = PositionWithDirection(position=snapped, direction=(-1, 0))
        draw_signal(surface, camera, signal_preview, color=RED, offset=True)

    else:
        if map.has_signal_at(snapped):
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
