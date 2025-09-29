import pygame
from models.construction import ConstructionMode
from config.colors import BLACK, RED, YELLOW, WHITE
from config.paths import CONSTRUCTION_MODE_ICONS
from config.settings import CONSTRUCTION_BUTTON_SIZE


def get_zoom_box(surface: pygame.Surface) -> pygame.Rect:
    return pygame.Rect(surface.get_width() - 100, 10, 80, 30)


def load_construction_icons():
    icon_cache = {}
    for mode in ConstructionMode:
        icon_path = CONSTRUCTION_MODE_ICONS[mode.name]
        icon = pygame.image.load(icon_path).convert_alpha()
        icon = pygame.transform.scale(icon, (CONSTRUCTION_BUTTON_SIZE*0.8, CONSTRUCTION_BUTTON_SIZE*0.8))

        # Make a new surface with black background (no transparency)
        colored_icon = pygame.Surface(icon.get_size())

        # Draw white using original alpha as mask
        for x in range(icon.get_width()):
            for y in range(icon.get_height()):
                _, _, _, alpha = icon.get_at((x, y))
                if alpha > 0:
                    colored_icon.set_at((x, y), WHITE)

        icon_cache[mode] = colored_icon

    return icon_cache


def get_construction_buttons(surface: pygame.Surface) -> list[tuple[ConstructionMode, pygame.Rect]]:
    button_margin = CONSTRUCTION_BUTTON_SIZE // 5
    w, h = surface.get_size()
    buttons = []
    for i, mode in enumerate(ConstructionMode):
        rect = pygame.Rect(
            button_margin + i * (CONSTRUCTION_BUTTON_SIZE + button_margin),
            h - CONSTRUCTION_BUTTON_SIZE - button_margin,
            CONSTRUCTION_BUTTON_SIZE,
            CONSTRUCTION_BUTTON_SIZE
        )
        buttons.append((mode, rect))
    return buttons

def draw_construction_buttons(surface, mode: ConstructionMode, icon_cache):
    buttons = get_construction_buttons(surface)
    for m, btn_rect in buttons:
        # Draw a solid background for the button (not transparent)
        pygame.draw.rect(surface, BLACK, btn_rect, border_radius=10)

        icon = icon_cache[m]
        icon_rect = icon.get_rect(center=btn_rect.center)
        surface.blit(icon, icon_rect)

        if m == mode:
            color = YELLOW if not mode is ConstructionMode.BULLDOZE else RED
            pygame.draw.rect(surface, color, btn_rect.inflate(10, 10), 5, border_radius=10)
        else:
            pygame.draw.rect(surface, WHITE, btn_rect.inflate(-2, -2), 1, border_radius=10)


def draw_zoom_indicator(surface, camera):
    if camera.scale != 1.0 or camera.x != 0 or camera.y != 0:
        zoom_text = f"{int(camera.scale * 100)}%"
        zoom_font = pygame.font.SysFont(None, 24)
        zoom_surface = zoom_font.render(zoom_text, True, WHITE)
        zoom_box = get_zoom_box(surface)
        pygame.draw.rect(surface, (50, 50, 50), zoom_box, border_radius=4)
        pygame.draw.rect(surface, (150, 150, 150), zoom_box, 2, border_radius=4)
        surface.blit(zoom_surface, zoom_surface.get_rect(center=zoom_box.center))
