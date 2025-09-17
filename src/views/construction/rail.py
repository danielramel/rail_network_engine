import pygame
from utils import snap_to_grid
from config.colors import GRAY
from graphics.camera import Camera
from models.network import RailNetwork, find_path
from models.construction import ConstructionState


def render_rail_construction(surface : pygame.Surface, camera: Camera, state: ConstructionState, network: RailNetwork):
    # Draw preview polyline
    if state.construction_anchor is None:
        return

    snapped = snap_to_grid(*camera.screen_to_world(*pygame.mouse.get_pos()))
    found_path = find_path(state.construction_anchor, snapped)
    screen_points = [camera.world_to_screen(pt.x, pt.y) for pt in found_path]
    if len(screen_points) >= 2:
        pygame.draw.lines(surface, GRAY, False, screen_points, max(1, int(3 * camera.scale)))