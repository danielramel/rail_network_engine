import pygame
from models.railway_system import RailwaySystem
from graphics.icon_loader import IconLoader
from models.geometry.position import Position
from ui.models.rectangle import RectangleUIComponent
from config.colors import BLACK, GREEN, WHITE, YELLOW, RED
from config.paths import ICON_PATHS
from config.settings import BUTTON_SIZE
from views.timetable.timetable_view import TimetableWindow


class TimeTableButton(RectangleUIComponent):
    handled_events = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL, pygame.KEYDOWN]
    def __init__(self, surface: pygame.Surface, railway: RailwaySystem):
        self._railway = railway

        self.icon = IconLoader().get_icon(ICON_PATHS["TIMETABLE"], BUTTON_SIZE)
        rect = pygame.Rect(BUTTON_SIZE//5, 300, BUTTON_SIZE, BUTTON_SIZE)
        super().__init__(rect, surface)
        self.timetable_window = None  # Store window reference
        
    def process_event(self, event: pygame.event) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t and (event.mod & pygame.KMOD_CTRL):
                self.open_timetable_window()
                return True
            return False
        
        elif self._rect.collidepoint(*event.screen_pos):
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.open_timetable_window()
            return True
        return False
    
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
        icon_rect = self.icon.get_rect(center=self._rect.center)
        self._surface.blit(self.icon, icon_rect)
        pygame.draw.rect(self._surface, WHITE, self._rect, 2, border_radius=10)