from core.config.color import Color
from core.graphics.camera import Camera
from core.models.geometry.position import Position
import pygame


def draw_node(screen: pygame.Surface, position: Position, camera: Camera, color=Color.WHITE, junction=False) -> None:
    """Draw a node on the given screen using the camera."""
    screen_x, screen_y = camera.world_to_screen(position)
    if junction:
        outer_radius = int(2 * camera.scale)
        inner_radius = int(1 * camera.scale)
    else:
        outer_radius = max(2, int(6 * camera.scale))
        inner_radius = max(1, int(3 * camera.scale))
    pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), outer_radius)
    pygame.draw.circle(screen, Color.BLACK, (int(screen_x), int(screen_y)), inner_radius)