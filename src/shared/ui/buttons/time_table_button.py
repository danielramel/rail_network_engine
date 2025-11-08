import pygame
from core.models.railway.railway_system import RailwaySystem
from core.graphics.icon_loader import IconLoader
from core.models.geometry.position import Position
from shared.ui.models.rectangle import RectangleUIComponent
from core.config.colors import BLACK, GREEN, WHITE, YELLOW, RED
from core.config.paths import ICON_PATHS
from core.config.settings import BUTTON_SIZE
from modules.timetable.views.timetable_view import TimetableWindow
from core.models.event import Event
from shared.ui.models.shortcut_ui_component import ShortcutUIComponent
from shared.ui.models.clickable_ui_component import ClickableUIComponent


class TimeTableButton(RectangleUIComponent, ShortcutUIComponent, ClickableUIComponent):
    def __init__(self, surface: pygame.Surface, railway: RailwaySystem):
        self._railway = railway

        self._icon = IconLoader().get_icon(ICON_PATHS["TIMETABLE"], BUTTON_SIZE)
        rect = pygame.Rect(BUTTON_SIZE//5, 300, BUTTON_SIZE, BUTTON_SIZE)
        super().__init__(rect, surface)
        self.timetable_window = None  # Store window reference
        self._shortcuts = {
            (pygame.K_t, False): self.open_timetable_window
        }

    def _on_click(self, event: Event) -> bool:
        if event.is_left_click:
            self.open_timetable_window()
    
    def open_timetable_window(self):
        if self.timetable_window is None:
            self.timetable_window = TimetableWindow(self._railway)
            self.timetable_window.window_closed.connect(self._on_timetable_window_closed)
            self.timetable_window.show()
        else:
            if self.timetable_window.isMinimized():
                self.timetable_window.showNormal()
            self.timetable_window.raise_()
            self.timetable_window.activateWindow()
    
    def _on_timetable_window_closed(self, *args, **kwargs):
            self.timetable_window = None

    def render(self, screen_pos: Position) -> None:
        pygame.draw.rect(self._surface, BLACK, self._rect, border_radius=10)
        icon_rect = self._icon.get_rect(center=self._rect.center)
        self._surface.blit(self._icon, icon_rect)
        pygame.draw.rect(self._surface, WHITE, self._rect, 2, border_radius=10)