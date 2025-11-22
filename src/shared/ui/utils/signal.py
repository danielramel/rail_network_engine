import pygame
from core.models.geometry.position import Position
from core.models.geometry.pose import Pose
from core.graphics.camera import Camera
from core.config.color import Color
from shared.ui.utils.nodes import draw_node

import pygame
import math

ANGLE_MAP = {
    (0, 1): 0,
    (-1, 1): 45,
    (-1, 0): 90,
    (-1, -1): 135,
    (0, -1): 180,
    (1, -1): 225,
    (1, 0): 270,
    (1, 1): 315
}


def draw_signal(screen: pygame.Surface, alignment: Pose, camera: Camera, color=Color.WHITE):
    """Draw a signal triangle at the given position and orientation."""
    size = int(20 * camera.scale)

    # local triangle points with origin at TOP vertex
    h = size // 2
    local_pts = [
        (0, -size),   # top point (anchor)
        (-h, 0),      # bottom-left
        (h, 0)        # bottom-right
    ]


    angle_deg = ANGLE_MAP[tuple(alignment.direction)] + 180
    ang = math.radians(angle_deg)

    cos_a = math.cos(ang)
    sin_a = math.sin(ang)

    # rotate local points
    rot_pts = []
    for x, y in local_pts:
        rx = x * cos_a - y * sin_a
        ry = x * sin_a + y * cos_a
        rot_pts.append((rx, ry))

    # translate so anchor is exactly at world → screen position
    sx, sy = camera.world_to_screen(alignment.node)
    scr_pts = [(sx + px, sy + py) for px, py in rot_pts]

    pygame.draw.polygon(screen, Color.BLACK, scr_pts)
    pygame.draw.polygon(screen, color, scr_pts, 2)