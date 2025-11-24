import pygame
from core.models.railway.railway_system import RailwaySystem
from core.graphics.icon_loader import IconLoader
from core.models.geometry.position import Position
from shared.ui.models.rectangle import RectangleUIComponent
from core.config.color import Color
from core.config.paths import ICON_PATHS
from core.config.settings import Config
from modules.route.route_window import RouteWindow
from core.models.event import Event
from shared.ui.models.shortcut_ui_component import ShortcutUIComponent
from shared.ui.models.clickable_ui_component import ClickableUIComponent


class RouteButton(RectangleUIComponent, ShortcutUIComponent, ClickableUIComponent):
    def __init__(self, screen: pygame.Surface, railway: RailwaySystem):
        self._railway = railway

        self._icon = IconLoader().get_icon(ICON_PATHS["ROUTE"], Config.BUTTON_SIZE)
        rect = pygame.Rect(Config.BUTTON_SIZE//5, 300, Config.BUTTON_SIZE, Config.BUTTON_SIZE)
        super().__init__(rect, screen)
        self.route_window = None  # Store window reference
        self._shortcuts = {
            (pygame.K_t, False): self.open_route_window
        }

    def _on_click(self, event: Event) -> bool:
        if event.is_left_click:
            self.open_route_window()
    
    def open_route_window(self):
        if self.route_window is None:
            self.route_window = RouteWindow(self._railway)
            self.route_window.window_closed.connect(self._on_route_window_closed)
            self.route_window.show()
        else:
            if self.route_window.isMinimized():
                self.route_window.showNormal()
            self.route_window.raise_()
            self.route_window.activateWindow()
    
    def _on_route_window_closed(self, *args, **kwargs):
            self.route_window = None

    def render(self, screen_pos: Position) -> None:
        pygame.draw.rect(self._screen, Color.BLACK, self._rect, border_radius=10)
        icon_rect = self._icon.get_rect(center=self._rect.center)
        self._screen.blit(self._icon, icon_rect)
        pygame.draw.rect(self._screen, Color.WHITE, self._rect, 2, border_radius=10)