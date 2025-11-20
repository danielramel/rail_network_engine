import pygame
from core.models.geometry.position import Position
from core.models.geometry.pose import Pose
from core.graphics.camera import Camera
from core.config.color import Color
from core.config.settings import Settings
from shared.ui.utils.nodes import draw_node


def draw_triangle(surface: pygame.Surface, alignment: Pose, camera: Camera, color=Color.WHITE, size_factor=1.0):
    def get_rotation_angle(direction_vector):
        angle_map = {
            (0, 1): 0,
            (1, 1): 45,
            (1, 0): 90,
            (1, -1): 135,
            (0, -1): 180,
            (-1, -1): 225,
            (-1, 0): 270,
            (-1, 1): 315
        }
        return angle_map[tuple(direction_vector)]

    base_size = int(25 * camera.scale)
    size = int(base_size * size_factor)
    screen_x, screen_y = camera.world_to_screen(alignment.position)

    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    h = size // 2
    points = [
        (h, 0),           # Top point
        (0, size - 1),    # Bottom left
        (2 * h, size - 1) # Bottom right
    ]
    pygame.draw.polygon(surf, Color.BLACK, points)
    pygame.draw.polygon(surf, color, points, 2)

    rotated_surf = pygame.transform.rotate(surf, 180+get_rotation_angle(alignment.direction))

    rect = rotated_surf.get_rect(center=(screen_x, screen_y))
    surface.blit(rotated_surf, rect)


def draw_signal(surface: pygame.Surface, alignment: Pose, camera: Camera, color=Color.WHITE, offset=False):
    """Draw a signal triangle at the given position and orientation."""
    if offset:
        draw_node(surface, alignment.position, camera, color=Color.YELLOW)
        # Adjust the position for the offset
        offset_y = Settings.GRID_SIZE * camera.scale / 1.25
        offset_position = Position(alignment.position.x, alignment.position.y - offset_y / camera.scale)
        offset_alignment = Pose(offset_position, alignment.direction)
        draw_triangle(surface, offset_alignment, camera, color=color, size_factor=1.0)
    else:
        draw_triangle(surface, alignment, camera, color=color, size_factor=1.0)

    
