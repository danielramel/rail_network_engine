# view (updated)
import pygame
from config.colors import RED, YELLOW
from graphics.camera import Camera
from domain.rail_map import RailMap
from ui.utils import draw_signal
from models.geometry import Position
from services.construction.signal_target import find_signal_target

def render_signal_preview(surface: pygame.Surface, world_pos: Position, map: RailMap, camera: Camera):
    target = find_signal_target(map, world_pos)
    if target.preview_pose is None:
        return

    color = RED if target.kind == 'invalid' else YELLOW
    draw_signal(surface, target.preview_pose, camera, color=color, offset=target.offset)
