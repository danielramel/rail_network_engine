from core.config.color import Color
from core.graphics.camera import Camera
from core.models.geometry.position import Position
import pygame


def draw_node(surface: pygame.Surface, node: Position, camera: Camera, color=Color.WHITE, junction=False) -> None:
    """Draw a node on the given surface using the camera."""
    screen_x, screen_y = camera.world_to_screen(node)
    if junction:
        outer_radius = int(2 * camera.scale)
        inner_radius = int(1 * camera.scale)
    else:
        outer_radius = max(2, int(6 * camera.scale))
        inner_radius = max(1, int(3 * camera.scale))
    pygame.draw.circle(surface, color, (int(screen_x), int(screen_y)), outer_radius)
    pygame.draw.circle(surface, Color.BLACK, (int(screen_x), int(screen_y)), inner_radius)