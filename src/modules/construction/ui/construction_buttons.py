import pygame
from core.graphics.icon_loader import IconLoader
from core.models.geometry.position import Position
from shared.ui.models.ui_component import UIComponent
from core.config.colors import BLACK, WHITE, YELLOW, RED
from modules.construction.construction_state import ConstructionMode, ConstructionState
from core.config.paths import ICON_PATHS
from core.config.settings import BUTTON_SIZE
from core.config.keyboard_shortcuts import CONSTRUCTION_MODE_SELECTION


class ConstructionButtons(UIComponent):
    handled_events = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL, pygame.KEYDOWN]
    def __init__(self, surface: pygame.Surface, construction_state: ConstructionState):
        self.icon_cache = {
            mode: IconLoader().get_icon(ICON_PATHS[mode.name], BUTTON_SIZE)
            for mode in ConstructionMode
        }
        self.buttons = self._get_buttons(surface)
        self.construction_state = construction_state
        self._surface = surface
        
        
    def process_event(self, event: pygame.event) -> bool:   
        if event.type == pygame.KEYDOWN:
            if event.key in CONSTRUCTION_MODE_SELECTION:
                self.construction_state.switch_mode(CONSTRUCTION_MODE_SELECTION[event.key])
                return True
            return False
             
        for mode, btn in self.buttons:
            if btn.collidepoint(*event.screen_pos):
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.construction_state.switch_mode(mode)
                return True
        return False

    def render(self, screen_pos: Position) -> None:
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

    def contains(self, screen_pos: Position) -> bool:
        return any(btn.collidepoint(*screen_pos) for _, btn in self.buttons)


    def _get_buttons(self, surface: pygame.Surface) -> list[tuple[ConstructionMode, pygame.Rect]]:
        button_margin = BUTTON_SIZE // 5
        _, h = surface.get_size()
        buttons = []
        for i, mode in enumerate(ConstructionMode):
            offset = (BUTTON_SIZE + button_margin) * i
            if mode is ConstructionMode.BULLDOZE:
                offset += (BUTTON_SIZE + button_margin)
            rect = pygame.Rect(
                button_margin + offset,
                h - BUTTON_SIZE - button_margin,
                BUTTON_SIZE,
                BUTTON_SIZE
            )
            buttons.append((mode, rect))
        return buttons