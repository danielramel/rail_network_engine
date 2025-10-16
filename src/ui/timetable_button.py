import pygame
from graphics.icon_loader import IconLoader
from models.geometry.position import Position
from ui.components.rectangle import RectangleUIComponent
from config.colors import BLACK, GREEN, WHITE, YELLOW, RED
from config.paths import TIMETABLE_ICON_PATH
from config.settings import BUTTON_SIZE
from ui.popups import alert


class TimeTableButton(RectangleUIComponent):
    handled_events = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL]
    def __init__(self, surface: pygame.Surface):
        self.icon = IconLoader().get_icon(TIMETABLE_ICON_PATH, BUTTON_SIZE)
        rect = pygame.Rect(BUTTON_SIZE//5, 300, BUTTON_SIZE, BUTTON_SIZE)
        super().__init__(rect, surface)
        
        
        
    def handle_event(self, event: pygame.event) -> bool:
        if self._rect.collidepoint(*event.pos):
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                alert("Timetable mode not implemented yet!")
            return True
        return False

    def render(self, screen_pos: Position) -> None:
        pygame.draw.rect(self._surface, BLACK, self._rect, border_radius=10)

        icon_rect = self.icon.get_rect(center=self._rect.center)
        self._surface.blit(self.icon, icon_rect)

        pygame.draw.rect(self._surface, WHITE, self._rect, 2, border_radius=10)