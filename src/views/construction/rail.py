import pygame
from config.colors import BLACK, RED, WHITE, YELLOW
from graphics.camera import Camera
from models.map import RailMap
from ui.utils import draw_node
from models.geometry import Position, Pose


def render_rail_preview(surface : pygame.Surface, world_pos: Position, anchor: Pose, map: RailMap, camera: Camera):
    snapped = world_pos.snap_to_grid()
    if map.is_blocked(snapped):
        draw_node(surface, snapped, camera, color=RED)
        if anchor is not None:
            draw_node(surface, anchor.position, camera, color=RED)
        return

    if anchor is None:
        draw_node(surface, snapped, camera, color=YELLOW)
        return

    if anchor.position == snapped:
        draw_node(surface, snapped, camera, color=YELLOW)
        return

    found_path = map.find_path(anchor, snapped)
    if not found_path:
        draw_node(surface, snapped, camera, color=RED)
        draw_node(surface, anchor.position, camera, color=RED)
        return
    
    
    screen_points = [tuple(camera.world_to_screen(Position(*pt))) for pt in found_path]
    pygame.draw.aalines(surface, YELLOW, False, screen_points)
    draw_node(surface, snapped, camera, color=YELLOW)
    draw_node(surface, anchor.position, camera, color=YELLOW)



def draw_rail_panel(surface: pygame.Surface, state: dict[str, Pose | int | None]):
    """Draw a construction information panel in the middle bottom of the screen"""
    # Panel dimensions
    panel_width = 400
    panel_height = 120
    padding = 15
    
    # Position in middle bottom
    screen_width, screen_height = surface.get_size()
    panel_x = (screen_width - panel_width) // 2
    panel_y = screen_height - panel_height - 15
    
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    
    pygame.draw.rect(surface, BLACK, panel_rect, border_radius=8)
    pygame.draw.rect(surface, WHITE, panel_rect, 2, border_radius=8)
    
    # Font setup
    title_font = pygame.font.SysFont(None, 28)
    data_font = pygame.font.SysFont(None, 22)
    
    # Draw title
    title_surface = title_font.render("Rail Construction", True, YELLOW)
    title_rect = title_surface.get_rect(centerx=panel_rect.centerx, top=panel_rect.top + padding)
    surface.blit(title_surface, title_rect)
    
    # Draw track speed adjustment controls
    label_surface = data_font.render("Track speed:", True, WHITE)
    label_rect = label_surface.get_rect(left=panel_rect.left + padding, top=title_rect.bottom + 20)
    surface.blit(label_surface, label_rect)

    # Button dimensions
    button_size = 32
    button_y = label_rect.top - 4
    minus_x = label_rect.right + 20
    plus_x = minus_x + button_size + 60

    # Draw minus button with border
    minus_rect = pygame.Rect(minus_x, button_y, button_size, button_size)
    pygame.draw.rect(surface, BLACK, minus_rect, border_radius=6)
    pygame.draw.rect(surface, WHITE, minus_rect, width=2, border_radius=6)
    minus_text = data_font.render("-", True, WHITE)
    minus_text_rect = minus_text.get_rect(center=minus_rect.center)
    surface.blit(minus_text, minus_text_rect)

    # Draw speed value
    speed_surface = data_font.render(str(state['track_speed']), True, YELLOW)
    speed_rect = speed_surface.get_rect(center=(minus_rect.right + 40, minus_rect.centery))
    surface.blit(speed_surface, speed_rect)

    # Draw plus button with border
    plus_rect = pygame.Rect(plus_x, button_y, button_size, button_size)
    pygame.draw.rect(surface, BLACK, plus_rect, border_radius=6)
    pygame.draw.rect(surface, WHITE, plus_rect, width=2, border_radius=6)
    plus_text = data_font.render("+", True, WHITE)
    plus_text_rect = plus_text.get_rect(center=plus_rect.center)
    surface.blit(plus_text, plus_text_rect)