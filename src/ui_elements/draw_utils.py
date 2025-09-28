
from turtle import color
import pygame
from config.colors import WHITE, BLACK, YELLOW

from config.settings import GRID_SIZE, STATION_RECT_SIZE
from graphics.camera import Camera
from models.position import Position, PositionWithDirection

def draw_node(surface: pygame.Surface, camera: Camera, node: Position, color=WHITE):
    """Draw a node on the given surface using the camera."""
    screen_x, screen_y = camera.world_to_screen(node)
    outer_radius = max(2, int(6 * camera.scale))
    inner_radius = max(1, int(3 * camera.scale))
    pygame.draw.circle(surface, color, (int(screen_x), int(screen_y)), outer_radius)
    pygame.draw.circle(surface, BLACK, (int(screen_x), int(screen_y)), inner_radius)


def draw_signal(surface: pygame.Surface, camera: Camera, alignment: PositionWithDirection, color=WHITE, offset=False):
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
        return angle_map[direction_vector]

    size = max(18, int(36 * camera.scale))
    screen_x, screen_y = camera.world_to_screen(alignment.position)

    if offset:
        draw_node(surface, camera, alignment.position, color=YELLOW)
        screen_y -= GRID_SIZE * camera.scale//1.25

    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    h = size // 2
    points = [
        (h, 0),           # Top point
        (0, size - 1),    # Bottom left
        (2 * h, size - 1) # Bottom right
    ]
    pygame.draw.polygon(surf, BLACK, points)
    pygame.draw.polygon(surf, color, points, 2)

    rotated_surf = pygame.transform.rotate(surf, get_rotation_angle(alignment.direction))

    rect = rotated_surf.get_rect(center=(screen_x, screen_y))
    surface.blit(rotated_surf, rect)
    
    
def draw_station(surface: pygame.Surface, camera: Camera, position: Position, name, color=WHITE):
    w, h = STATION_RECT_SIZE
    rect = pygame.Rect(0, 0, w * camera.scale, h * camera.scale)
    rect.center = tuple(camera.world_to_screen(position))
    pygame.draw.rect(surface, color, rect, 3)

    # Render station name text in the middle of the rect
    font = pygame.font.SysFont(None, int(rect.height * 0.6))
    text_surface = font.render(name, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_dashed_line(surface: pygame.Surface, start_pos, end_pos, color, width=1, dash_length=10, gap_length=5):
    """Draw a dashed line on the surface from start_pos to end_pos."""
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1
    distance = (dx**2 + dy**2) ** 0.5
    if distance == 0:
        return
    dash_count = int(distance // (dash_length + gap_length))
    for i in range(dash_count + 1):
        start_x = x1 + (dx * (i * (dash_length + gap_length)) / distance)
        start_y = y1 + (dy * (i * (dash_length + gap_length)) / distance)
        end_x = x1 + (dx * min((i * (dash_length + gap_length) + dash_length) / distance, 1))
        end_y = y1 + (dy * min((i * (dash_length + gap_length) + dash_length) / distance, 1))
        pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), width)