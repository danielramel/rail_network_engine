import pygame
from core.graphics.icon_loader import IconLoader
from core.models.event import Event
from core.models.geometry.position import Position
from modules.setup.train_placement.models.train_placement_state import TrainPlacementTool, TrainPlacementState
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from core.config.color import Color
from core.config.paths import ICON_PATHS
from core.config.settings import Config
from shared.ui.models.shortcut_ui_component import ShortcutUIComponent
from core.config.keyboard_shortcuts import TRAIN_PLACEMENT_TOOL_SELECTION


class TrainPlacementButtons(ShortcutUIComponent, ClickableUIComponent):
    def __init__(self, screen: pygame.Surface, state: TrainPlacementState):
        self.icon_cache = {
            tool: IconLoader().get_icon(ICON_PATHS[tool.name], Config.BUTTON_SIZE)
            for tool in TrainPlacementTool
        }
        self.buttons = self._get_buttons(screen)
        self._state = state
        self._screen = screen
        
        self._shortcuts = {
            (key, False): lambda tool=tool: self._state.switch_tool(tool)
            for key, tool in TRAIN_PLACEMENT_TOOL_SELECTION.items()
        }
        
    def _on_click(self, event: Event) -> bool:
        if not event.is_left_click:
            return False
        for tool, btn in self.buttons:
            if btn.collidepoint(*event.screen_pos):
                self._state.switch_tool(tool)
                return True
        return False

    def render(self, screen_pos: Position | None) -> None:
        for tool, btn_rect in self.buttons:
            bg_color = Color.DARKGREY if screen_pos is not None and btn_rect.collidepoint(*screen_pos) else Color.BLACK 
            pygame.draw.rect(self._screen, bg_color, btn_rect, border_radius=10)

            icon = self.icon_cache[tool]
            icon_rect = icon.get_rect(center=btn_rect.center)
            self._screen.blit(icon, icon_rect)

            if tool == self._state.tool:
                color = Color.YELLOW if not self._state.tool is TrainPlacementTool.REMOVE_TRAIN else Color.RED
                pygame.draw.rect(self._screen, color, btn_rect.inflate(5, 5), 5, border_radius=10)
            else:
                pygame.draw.rect(self._screen, Color.WHITE, btn_rect, 2, border_radius=10)

    def contains(self, screen_pos: Position) -> bool:
        return any(btn.collidepoint(*screen_pos) for _, btn in self.buttons)


    def _get_buttons(self, screen: pygame.Surface) -> list[tuple[TrainPlacementTool, pygame.Rect]]:
        button_margin = Config.BUTTON_SIZE // 5
        w, h = screen.get_size()
        buttons = []
        for i, tool in enumerate(TrainPlacementTool):
            rect = pygame.Rect(
                w - 2 * (Config.BUTTON_SIZE + button_margin) + (Config.BUTTON_SIZE + button_margin) * i,
                h - Config.BUTTON_SIZE - button_margin,
                Config.BUTTON_SIZE,
                Config.BUTTON_SIZE
            )
            buttons.append((tool, rect))
        return buttons