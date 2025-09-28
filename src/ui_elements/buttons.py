import pygame
from models.construction import ConstructionMode
from config.colors import RED, YELLOW, WHITE, GRAY


def get_zoom_box(surface: pygame.Surface) -> pygame.Rect:
    return pygame.Rect(surface.get_width() - 100, 10, 80, 30)

def get_construction_buttons(surface: pygame.Surface):
    button_size = 50
    button_margin = 10
    w, h = surface.get_size()
    buttons = []
    for i, mode in enumerate(ConstructionMode):
        rect = pygame.Rect(
            button_margin + i * (button_size + button_margin),
            h - button_size - button_margin,
            button_size,
            button_size
        )
        buttons.append((mode, rect))
    return buttons


def draw_construction_buttons(surface, state):
    font = pygame.font.SysFont(None, 40)
    for mode, rect in get_construction_buttons(surface):
        if state.Mode is ConstructionMode.BULLDOZE and mode is ConstructionMode.BULLDOZE:
            color = RED
        elif state.Mode is mode:
            color = YELLOW
        else:
            color = GRAY
        pygame.draw.rect(surface, color, rect, border_radius=8)
        text = font.render(mode.name[0], True, WHITE)
        surface.blit(text, text.get_rect(center=rect.center))

def draw_zoom_indicator(surface, camera):
    if camera.scale != 1.0 or camera.x != 0 or camera.y != 0:
        zoom_text = f"{int(camera.scale * 100)}%"
        zoom_font = pygame.font.SysFont(None, 24)
        zoom_surface = zoom_font.render(zoom_text, True, WHITE)
        zoom_box = get_zoom_box(surface)
        pygame.draw.rect(surface, (50, 50, 50), zoom_box, border_radius=4)
        pygame.draw.rect(surface, (150, 150, 150), zoom_box, 2, border_radius=4)
        surface.blit(zoom_surface, zoom_surface.get_rect(center=zoom_box.center))
