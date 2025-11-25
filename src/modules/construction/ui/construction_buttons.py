import pygame
from core.graphics.icon_loader import IconLoader
from core.models.event import Event
from core.models.geometry.position import Position
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from core.config.color import Color
from modules.construction.models.construction_state import ConstructionTool, ConstructionState
from core.config.paths import ICON_PATHS
from core.config.settings import Config
from core.config.keyboard_shortcuts import CONSTRUCTION_TOOL_SELECTION
from shared.ui.models.shortcut_ui_component import ShortcutUIComponent


class ConstructionButtons(ShortcutUIComponent, ClickableUIComponent):
    handled_events = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL, pygame.KEYDOWN]
    def __init__(self, screen: pygame.Surface, construction_state: ConstructionState):
        self.icon_cache = {
            tool: IconLoader().get_icon(ICON_PATHS[tool.name], Config.BUTTON_SIZE)
            for tool in ConstructionTool
        }
        self.buttons = self._get_buttons(screen)
        self.construction_state = construction_state
        self._screen = screen
        
        self._shortcuts = {
            (key, False): lambda tool=tool: self.construction_state.switch_tool(tool)
            for key, tool in CONSTRUCTION_TOOL_SELECTION.items()
        }
        
    def _on_click(self, event: Event) -> bool:
        if not event.is_left_click:
            return False
        for tool, btn in self.buttons:
            if btn.collidepoint(*event.screen_pos):
                self.construction_state.switch_tool(tool)
                return True
        return False

    def render(self, screen_pos: Position) -> None:
        for tool, btn_rect in self.buttons:
        # Draw a solid background for the button (not transparent)
            pygame.draw.rect(self._screen, Color.BLACK, btn_rect, border_radius=10)

            icon = self.icon_cache[tool]
            icon_rect = icon.get_rect(center=btn_rect.center)
            self._screen.blit(icon, icon_rect)

            if tool == self.construction_state.tool:
                color = Color.YELLOW if not self.construction_state.tool is ConstructionTool.BULLDOZE else Color.RED
                pygame.draw.rect(self._screen, color, btn_rect.inflate(10, 10), 5, border_radius=10)
            else:
                pygame.draw.rect(self._screen, Color.WHITE, btn_rect.inflate(-2, -2), 1, border_radius=10)

    def contains(self, screen_pos: Position) -> bool:
        return any(btn.collidepoint(*screen_pos) for _, btn in self.buttons)


    def _get_buttons(self, screen: pygame.Surface) -> list[tuple[ConstructionTool, pygame.Rect]]:
        button_margin = Config.BUTTON_SIZE // 5
        w, h = screen.get_size()
        buttons = []
        for i, tool in enumerate(ConstructionTool):
            offset = (Config.BUTTON_SIZE + button_margin) * i
            if tool is ConstructionTool.BULLDOZE:
                offset += (Config.BUTTON_SIZE + button_margin)
            rect = pygame.Rect(
                w - 7 * (Config.BUTTON_SIZE + button_margin) + offset,
                h - Config.BUTTON_SIZE - button_margin,
                Config.BUTTON_SIZE,
                Config.BUTTON_SIZE
            )
            buttons.append((tool, rect))
        return buttons