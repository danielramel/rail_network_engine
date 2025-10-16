import pygame
from graphics.icon_loader import IconLoader
from models.geometry.position import Position
from ui.components.rectangle import RectangleUIComponent
from config.colors import BLACK, GREEN, WHITE, YELLOW, RED
from config.paths import TIMETABLE_ICON_PATH
from config.settings import BUTTON_SIZE
from views.timetable.timetable_view import TimetableWindow


class TimeTableButton(RectangleUIComponent):
    handled_events = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL]
    def __init__(self, surface: pygame.Surface, train_repository):
        self.train_repository = train_repository
        
        self.icon = IconLoader().get_icon(TIMETABLE_ICON_PATH, BUTTON_SIZE)
        rect = pygame.Rect(BUTTON_SIZE//5, 300, BUTTON_SIZE, BUTTON_SIZE)
        super().__init__(rect, surface)
        self.timetable_window = None  # Store window reference
        
    def handle_event(self, event: pygame.event) -> bool:
        if self._rect.collidepoint(*event.pos_):
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.timetable_window is None:
                    self.timetable_window = TimetableWindow(self.train_repository)
                    # Connect to the custom signal instead
                    self.timetable_window.window_closed.connect(self._on_timetable_window_closed)
                    self.timetable_window.show()
                else:
                    if self.timetable_window.isMinimized():
                        self.timetable_window.showNormal()
                    self.timetable_window.raise_()
                    self.timetable_window.activateWindow()
            return True
        return False
    
    def _on_timetable_window_closed(self, *args, **kwargs):
            self.timetable_window = None
            print("Timetable window closed")

    def render(self, screen_pos: Position) -> None:
        pygame.draw.rect(self._surface, BLACK, self._rect, border_radius=10)
        icon_rect = self.icon.get_rect(center=self._rect.center)
        self._surface.blit(self.icon, icon_rect)
        pygame.draw.rect(self._surface, WHITE, self._rect, 2, border_radius=10)