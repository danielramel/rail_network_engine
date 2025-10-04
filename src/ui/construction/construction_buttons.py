from models.geometry.position import Position
from ui.core.ui_element import UIElement
import pygame
from config.colors import BLACK, WHITE, YELLOW, RED
from models.construction import ConstructionMode, ConstructionState
from config.paths import CONSTRUCTION_MODE_ICONS
from config.settings import CONSTRUCTION_BUTTON_SIZE


class ConstructionButtons(UIElement):
    def __init__(self, surface: pygame.Surface, construction_state: ConstructionState):
        self.icon_cache = self._load_icons()
        self.buttons = self._get_buttons(surface)
        self.construction_state = construction_state
        self._surface = surface

    def contains(self, pos):
        return any(btn.collidepoint(pos.x, pos.y) for _, btn in self.buttons)
    
    def handle_click(self, pos: Position) -> bool:
        for mode, btn in self.buttons:
            if btn.collidepoint(pos.x, pos.y):
                self.construction_state.switch_mode(mode)
                return True
        return False

    def draw(self) -> None:
        for mode, btn_rect in self.buttons:
        # Draw a solid background for the button (not transparent)
            pygame.draw.rect(self._surface, BLACK, btn_rect, border_radius=10)

            icon = self.icon_cache[mode]
            icon_rect = icon.get_rect(center=btn_rect.center)
            self._surface.blit(icon, icon_rect)

            if mode == self.construction_state.mode:
                color = YELLOW if not self.construction_state.mode is ConstructionMode.BULLDOZE else RED
                pygame.draw.rect(self._surface, color, btn_rect.inflate(10, 10), 5, border_radius=10)
            else:
                pygame.draw.rect(self._surface, WHITE, btn_rect.inflate(-2, -2), 1, border_radius=10)

    @staticmethod
    def _get_buttons(surface: pygame.Surface) -> list[tuple[ConstructionMode, pygame.Rect]]:
        button_margin = CONSTRUCTION_BUTTON_SIZE // 5
        _, h = surface.get_size()
        buttons = []
        for i, mode in enumerate(ConstructionMode):
            offset = (CONSTRUCTION_BUTTON_SIZE + button_margin) * i
            if mode is ConstructionMode.BULLDOZE:
                offset += (CONSTRUCTION_BUTTON_SIZE + button_margin)
            rect = pygame.Rect(
                button_margin + offset,
                h - CONSTRUCTION_BUTTON_SIZE - button_margin,
                CONSTRUCTION_BUTTON_SIZE,
                CONSTRUCTION_BUTTON_SIZE
            )
            buttons.append((mode, rect))
        return buttons
    
    @staticmethod
    def _load_icons():
        icon_cache = {}
        for mode in ConstructionMode:
            icon_path = CONSTRUCTION_MODE_ICONS[mode.name]
            icon = pygame.image.load(icon_path).convert_alpha()
            icon = pygame.transform.scale(icon, (int(CONSTRUCTION_BUTTON_SIZE*0.8), int(CONSTRUCTION_BUTTON_SIZE*0.8)))

            # Create a new surface with white color and same alpha as the original icon
            colored_icon = pygame.Surface(icon.get_size(), pygame.SRCALPHA)
            colored_icon.fill(WHITE)  # fill with white

            # Use the original icon's alpha as mask
            alpha_mask = pygame.surfarray.pixels_alpha(icon)
            pygame.surfarray.pixels_alpha(colored_icon)[:] = alpha_mask

            icon_cache[mode] = colored_icon

        return icon_cache