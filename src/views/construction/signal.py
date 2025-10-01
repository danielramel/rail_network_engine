import pygame
from models.geometry import Position, Pose
from ui_elements.draw_utils import draw_signal
from config.colors import GRAY, RED, YELLOW
from graphics.camera import Camera
from models.map import RailMap
from models.construction import ConstructionState


def render_signal_preview(surface : pygame.Surface, world_pos: Position, map: RailMap, camera: Camera):
    snapped = world_pos.snap_to_grid()

    if not map.has_node_at(snapped) or map.is_junction(snapped):
        signal_preview = Pose(position=snapped, direction=(-1, 0))
        draw_signal(surface, signal_preview, camera, color=RED, offset=True)

    else:
        if map.has_signal_at(snapped):
            if len(map._graph[snapped]) == 1:
                signal_preview = Pose(position=snapped, direction=map._graph.nodes[snapped]['signal'])
                draw_signal(surface, signal_preview, camera, color=YELLOW, offset=True)
                return # dead end, cannot toggle
            
            current_direction = map._graph.nodes[snapped]['signal']
            neighbors = tuple(map._graph.neighbors(snapped))
            if snapped.direction_to(neighbors[0]) == current_direction:
                signal_preview = Pose(position=snapped, direction=snapped.direction_to(neighbors[1]))
            else:
                signal_preview = Pose(position=snapped, direction=snapped.direction_to(neighbors[0]))

            draw_signal(surface, signal_preview, camera, color=YELLOW, offset=True)
        else:
            signal_preview = Pose(position=snapped, direction=snapped.direction_to(next(map._graph.neighbors(snapped))))
            draw_signal(surface, signal_preview, camera, color=YELLOW)
