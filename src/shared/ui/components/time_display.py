import pygame
from core.config.colors import BLACK, WHITE
from core.models.geometry.position import Position
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.models.rectangle import RectangleUIComponent
from core.models.time import Time
from shared.ui.utils.popups import user_input

class TimeDisplay(RectangleUIComponent, ClickableUIComponent):
    def __init__(self, time: Time, surface: pygame.Surface, modifiable: bool = False) -> None:
        self._rect = self._get_rect(surface)
        self._surface = surface
        self._time = time
        self._modifiable = modifiable

    def render(self, screen_pos: Position) -> None:
        font = pygame.font.SysFont("Courier New", 24)
        hours, minutes, secs = self._time.get_hours_minutes_seconds()

        # Draw black background with white border
        rect = self._get_rect(self._surface)
        pygame.draw.rect(self._surface, BLACK, rect)
        pygame.draw.rect(self._surface, WHITE, rect, 2, border_radius=5)
        time_text = f"{hours:02}:{minutes:02}:{secs:02}"
        text_surface = font.render(time_text, True, WHITE)
        rect = self._get_rect(self._surface)
        text_rect = text_surface.get_rect(center=rect.center)
        self._surface.blit(text_surface, text_rect)

    def _get_rect(self, surface: pygame.Surface) -> pygame.Rect:
        width, height = 130, 40
        x = (surface.get_width() - width) // 2
        y = 10
        return pygame.Rect(x, y, width, height)
    
    def _on_click(self, event) -> None:
        if not self._modifiable:
            return
        new_time = user_input("Enter time (HH:MM:SS): ")
        
        self._time.set_time_from_string(new_time)