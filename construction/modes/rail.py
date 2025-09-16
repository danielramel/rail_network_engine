from utils import get_direction_between_points, snap_to_grid
import pygame
from pathfinding import find_path
from colors import GRAY
from models import PointWithDirection

def handle_rail_click(state, camera, network, pos):
    snapped = snap_to_grid(*camera.screen_to_world(*pos))
    if state.construction_anchor is None:
        state.construction_anchor = PointWithDirection(snapped, (0,0))
    elif snapped == state.construction_anchor.point:
        state.construction_anchor = None
    else:
        found_path = find_path(state.construction_anchor, snapped)
        
        network.add_segment(
            network.add_node(found_path[0]),
            network.add_node(found_path[-1]),
            found_path
        )
        state.construction_anchor = PointWithDirection(snapped, get_direction_between_points(found_path[-2], snapped))

def render_rail_construction(surface, camera, state, network):
    # Draw preview polyline
    if state.construction_anchor is None:
        return

    snapped = snap_to_grid(*camera.screen_to_world(*pygame.mouse.get_pos()))
    found_path = find_path(state.construction_anchor, snapped)
    screen_points = [camera.world_to_screen(pt.x, pt.y) for pt in found_path]
    if len(screen_points) >= 2:
        pygame.draw.lines(surface, GRAY, False, screen_points, max(1, int(3 * camera.scale)))