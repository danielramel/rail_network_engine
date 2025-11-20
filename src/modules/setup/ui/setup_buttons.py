import pygame
from core.graphics.icon_loader import IconLoader
from core.models.event import Event
from core.models.geometry.position import Position
from modules.setup.models.setup_state import SetupTool, SetupState
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from core.config.color import Color
from core.config.paths import ICON_PATHS
from core.config.settings import Settings
from shared.ui.models.shortcut_ui_component import ShortcutUIComponent
from core.config.keyboard_shortcuts import SETUP_TOOL_SELECTION


class SetupButtons(ShortcutUIComponent, ClickableUIComponent):
    def __init__(self, surface: pygame.Surface, setup_state: SetupState):
        self.icon_cache = {
            tool: IconLoader().get_icon(ICON_PATHS[tool.name], Settings.BUTTON_SIZE)
            for tool in SetupTool
        }
        self.buttons = self._get_buttons(surface)
        self._state = setup_state
        self._surface = surface
        
        self._shortcuts = {
            (key, False): lambda tool=tool: self._state.switch_tool(tool)
            for key, tool in SETUP_TOOL_SELECTION.items()
        }
        
    def _on_click(self, event: Event) -> bool:
        if not event.is_left_click:
            return False
        for tool, btn in self.buttons:
            if btn.collidepoint(*event.screen_pos):
                self._state.switch_tool(tool)
                return True
        return False

    def render(self, screen_pos: Position) -> None:
        for tool, btn_rect in self.buttons:
        # Draw a solid background for the button (not transparent)
            pygame.draw.rect(self._surface, Color.BLACK, btn_rect, border_radius=10)

            icon = self.icon_cache[tool]
            icon_rect = icon.get_rect(center=btn_rect.center)
            self._surface.blit(icon, icon_rect)

            if tool == self._state.tool:
                color = Color.YELLOW if not self._state.tool is SetupTool.REMOVE_TRAIN else Color.RED
                pygame.draw.rect(self._surface, color, btn_rect.inflate(10, 10), 5, border_radius=10)
            else:
                pygame.draw.rect(self._surface, Color.WHITE, btn_rect.inflate(-2, -2), 1, border_radius=10)

    def contains(self, screen_pos: Position) -> bool:
        return any(btn.collidepoint(*screen_pos) for _, btn in self.buttons)


    def _get_buttons(self, surface: pygame.Surface) -> list[tuple[SetupTool, pygame.Rect]]:
        button_margin = Settings.BUTTON_SIZE // 5
        _, h = surface.get_size()
        buttons = []
        for i, tool in enumerate(SetupTool):
            rect = pygame.Rect(
                button_margin + (Settings.BUTTON_SIZE + button_margin) * i,
                h - Settings.BUTTON_SIZE - button_margin,
                Settings.BUTTON_SIZE,
                Settings.BUTTON_SIZE
            )
            buttons.append((tool, rect))
        return buttons