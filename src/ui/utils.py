import pygame
from config.colors import GREEN, LIME, PURPLE, LIGHTBLUE, RED, WHITE, BLACK, YELLOW

from config.settings import GRID_SIZE, STATION_RECT_SIZE
from graphics.camera import Camera
from models.construction_state import EdgeAction
from models.geometry import Position, Pose
from models.geometry.direction import Direction
from models.geometry.edge import Edge
from models.station import Station
from models.train import Train
import math

def draw_node(surface: pygame.Surface, node: Position, camera: Camera, color=WHITE):
    """Draw a node on the given surface using the camera."""
    screen_x, screen_y = camera.world_to_screen(node)
    outer_radius = max(2, int(6 * camera.scale))
    inner_radius = max(1, int(3 * camera.scale))
    pygame.draw.circle(surface, color, (int(screen_x), int(screen_y)), outer_radius)
    pygame.draw.circle(surface, BLACK, (int(screen_x), int(screen_y)), inner_radius)


def draw_triangle(surface: pygame.Surface, alignment: Pose, camera: Camera, color=WHITE, size_factor=1.0):
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
    pygame.draw.polygon(surf, BLACK, points)
    pygame.draw.polygon(surf, color, points, 2)

    rotated_surf = pygame.transform.rotate(surf, 180+get_rotation_angle(alignment.direction))

    rect = rotated_surf.get_rect(center=(screen_x, screen_y))
    surface.blit(rotated_surf, rect)


def draw_signal(surface: pygame.Surface, alignment: Pose, camera: Camera, color=WHITE, offset=False):
    """Draw a signal triangle at the given position and orientation."""
    screen_x, screen_y = camera.world_to_screen(alignment.position)

    if offset:
        draw_node(surface, alignment.position, camera, color=YELLOW)
        # Adjust the position for the offset
        offset_y = GRID_SIZE * camera.scale / 1.25
        offset_position = Position(alignment.position.x, alignment.position.y - offset_y / camera.scale)
        offset_alignment = Pose(offset_position, alignment.direction)
        draw_triangle(surface, offset_alignment, camera, color=color, size_factor=1.0)
    else:
        draw_triangle(surface, alignment, camera, color=color, size_factor=1.0)

    
def draw_station(surface: pygame.Surface, station: Station, camera: Camera, color=PURPLE):
    width = max(1, int(round(3 * camera.scale)))
    w, h = STATION_RECT_SIZE
    rect = pygame.Rect(0, 0, w * camera.scale, h * camera.scale)
    rect.center = tuple(camera.world_to_screen(station.position))
    pygame.draw.rect(surface, BLACK, rect)
    pygame.draw.rect(surface, color, rect, width)

    # Render station name text in the middle of the rect
    font = pygame.font.SysFont(None, int(rect.height * 0.6))
    text_surface = font.render(station.name, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_dotted_line(surface: pygame.Surface, start_pos: Position, end_pos: Position, camera: Camera, color):
    """Draw a dotted line on the surface from start_pos to end_pos."""
    start_pos = camera.world_to_screen(start_pos)
    end_pos = camera.world_to_screen(end_pos)

    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1
    distance = start_pos.distance_to(end_pos)
    dot_spacing = 4
    dot_count = math.ceil(distance / dot_spacing)
    for i in range(dot_count):
        dot_x = x1 + (dx * (i * dot_spacing) / distance)
        dot_y = y1 + (dy * (i * dot_spacing) / distance)
        pygame.draw.circle(surface, color, (int(dot_x), int(dot_y)), 1)

def draw_edge(surface: pygame.Surface, edge: Edge, camera: Camera, edge_type: EdgeAction, speed=None):
    # Line width scales with camera zoom; ensure at least 1 pixel
    width = max(1, int(round(3 * camera.scale)))

    start, end = camera.world_to_screen_from_edge(edge)

    if edge_type in (EdgeAction.BULLDOZE, EdgeAction.INVALID_PLATFORM):
        pygame.draw.line(surface, RED, start, end, width=width)

    elif edge_type == EdgeAction.PLATFORM_SELECTED:
        draw_platform(surface, edge, camera, color=LIGHTBLUE)

    elif edge_type == EdgeAction.PLATFORM:
        draw_platform(surface, edge, camera, color=PURPLE)

    elif edge_type == EdgeAction.LOCKED_PLATFORM:
        pygame.draw.line(surface, PURPLE, start, end, width=width)
        draw_platform(surface, edge, camera, color=LIME)

    elif edge_type == EdgeAction.LOCKED_PREVIEW:
        pygame.draw.line(surface, GREEN, start, end, width=width)

    elif edge_type == EdgeAction.LOCKED:
        pygame.draw.line(surface, LIME, start, end, width=width)

    elif edge_type == EdgeAction.NORMAL:
        draw_dotted_line(surface, edge.a, edge.b, camera, color=WHITE)
    
    elif edge_type == EdgeAction.SPEED:
        if speed is None:
            raise ValueError("Speed must be provided for SPEED edge type")
        color = color_from_speed(speed)
        pygame.draw.line(surface, color, start, end, width=width)

def draw_grid(surface, camera):
    """Draw grid lines with camera transform"""
    w, h = surface.get_size()
    
    # Calculate world bounds visible on screen
    world_left, world_top = camera.screen_to_world(Position(0, 0))
    world_right, world_bottom = camera.screen_to_world(Position(w, h))

    # Calculate grid line positions
    start_x = int(world_left // GRID_SIZE) * GRID_SIZE
    start_y = int(world_top // GRID_SIZE) * GRID_SIZE
    
    # Draw vertical grid lines
    x = start_x
    while x <= world_right + GRID_SIZE:
        screen_x, _ = camera.world_to_screen(Position(x, 0))
        if 0 <= screen_x <= w:
            pygame.draw.aaline(surface, (40, 40, 40), (screen_x, 0), (screen_x, h))
        x += GRID_SIZE
    
    # Draw horizontal grid lines
    y = start_y
    while y <= world_bottom + GRID_SIZE:
        _, screen_y = camera.world_to_screen(Position(0, y))
        if 0 <= screen_y <= h:
            pygame.draw.aaline(surface, (60, 60, 60), (0, screen_y), (w, screen_y))
        y += GRID_SIZE


def draw_platform(surface: pygame.Surface, edge: Edge, camera: Camera, color=PURPLE):
    a, b = edge
    offset = int(2 * camera.scale)  # pixels of separation
    # Calculate direction vector
    ax, ay = camera.world_to_screen(a)
    bx, by = camera.world_to_screen(b)
    dx, dy = bx - ax, by - ay
    length = (dx**2 + dy**2) ** 0.5
    if length != 0:
        # Perpendicular vector (normalized)
        perp_x = -dy / length
        perp_y = dx / length
    else:
        perp_x = perp_y = 0

    # Offset both lines in opposite perpendicular directions
    pygame.draw.aaline(
        surface, color,
        (ax + perp_x * offset, ay + perp_y * offset),
        (bx + perp_x * offset, by + perp_y * offset)
    )
    pygame.draw.aaline(
        surface, color,
        (ax - perp_x * offset, ay - perp_y * offset),
        (bx - perp_x * offset, by - perp_y * offset)
    )
        
        
def color_from_speed(speed: int) -> tuple[int, int, int]:
    """
    Map a speed value (0–200) to a visible RGB color.

    The gradient goes:
        Purple → Blue → Cyan → Green → Yellow → Red
    for maximum visual distinction.

    Returns:
        (R, G, B)
    """
    # Clamp to valid range
    speed = max(0, min(speed, 200))

    # Define color stops (speed, (R,G,B))
    gradient = [
        (10,  (0, 0, 255)),     # Blue
        (80,  (0, 255, 255)),   # Cyan
        (120, (0, 255, 0)),     # Green
        (150, (255, 255, 0)),   # Yellow
        (200,   (128, 0, 128)),   # Purple
    ]

    # Find which two stops we’re between
    for i in range(len(gradient) - 1):
        s0, c0 = gradient[i]
        s1, c1 = gradient[i + 1]
        if s0 <= speed <= s1:
            ratio = (speed - s0) / (s1 - s0)
            r = int(c0[0] + (c1[0] - c0[0]) * ratio)
            g = int(c0[1] + (c1[1] - c0[1]) * ratio)
            b = int(c0[2] + (c1[2] - c0[2]) * ratio)
            return (r, g, b)

    return gradient[-1][1]  # fallback

def draw_train_car(surface: pygame.Surface, edge: Edge, camera: Camera):
    a, b = edge
    ax, ay = camera.world_to_screen(a)
    bx, by = camera.world_to_screen(b)
    
    # Calculate direction vector
    dx, dy = bx - ax, by - ay
    length = math.sqrt(dx**2 + dy**2)
    
    if length == 0:
        return
    
    # Normalized direction and perpendicular vectors
    dir_x, dir_y = dx / length, dy / length
    perp_x, perp_y = -dir_y, dir_x
    
    # Rectangle width (perpendicular to the edge)
    width = 16 * camera.scale
    half_width = width / 2
    
    # Calculate the four corners of the rectangle
    points = [
        (ax + perp_x * half_width, ay + perp_y * half_width),
        (bx + perp_x * half_width, by + perp_y * half_width),
        (bx - perp_x * half_width, by - perp_y * half_width),
        (ax - perp_x * half_width, ay - perp_y * half_width)
    ]
    
    # Draw filled rectangle with border
    pygame.draw.polygon(surface, YELLOW, points)
    pygame.draw.polygon(surface, BLACK, points, 2)

def draw_train_lights(surface: pygame.Surface, world_pos: Position, direction: Direction,
                      camera: Camera, color: tuple):
    screen_x, screen_y = camera.world_to_screen(world_pos)

    # direction is a small vector like (dx, dy) with components in {-1, 0, 1}
    dx, dy = direction
    perp_x, perp_y = -dy, dx

    # spacing in screen pixels
    spacing = max(2, int(4 * camera.scale))
    radius = max(2, int(3 * camera.scale))

    left_x = int(screen_x + perp_x * -spacing)
    left_y = int(screen_y + perp_y * -spacing)
    right_x = int(screen_x + perp_x * spacing)
    right_y = int(screen_y + perp_y * spacing)


    pygame.draw.circle(surface, color, (left_x, left_y), radius)
    pygame.draw.circle(surface, color, (right_x, right_y), radius)


def draw_train(surface: pygame.Surface, train: Train, camera: Camera):
    if not train.path:
        return
    # Draw train cars
    occupied_edges = train.occupied_edges()
    for edge in occupied_edges:
        draw_train_car(surface, edge.move(edge.direction, train.edge_progress*GRID_SIZE), camera)

    last_edge = occupied_edges[-1]
    back_pos = last_edge.move(last_edge.direction, train.edge_progress*GRID_SIZE).a
    direction = last_edge.direction.opposite()
    draw_train_lights(surface, back_pos, direction, camera, color=RED)
    
    # draw current speed above the train front
    speed_text = f"{int(round(train.speed))} km/h"
    font_size = max(12, int(16 * camera.scale))
    font = pygame.font.SysFont(None, font_size)

    text_fg = font.render(speed_text, True, WHITE)
    text_bg = font.render(speed_text, True, BLACK)

    first_edge = occupied_edges[0]
    front_pos = first_edge.move(first_edge.direction, train.edge_progress*GRID_SIZE).b
    sx, sy = camera.world_to_screen(front_pos)
    offset_y = int(18 * camera.scale)

    bg_rect = text_bg.get_rect(center=(sx + 1, sy - offset_y + 1))
    fg_rect = text_fg.get_rect(center=(sx, sy - offset_y))

    surface.blit(text_bg, bg_rect)
    surface.blit(text_fg, fg_rect)
