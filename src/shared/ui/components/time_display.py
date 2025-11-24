import pygame
from core.config.color import Color
from core.graphics.graphics_context import GraphicsContext
from core.models.geometry.position import Position
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.models.rectangle import RectangleUIComponent
from core.models.time import Time

class TimeDisplay(RectangleUIComponent):
    def __init__(self, time: Time, graphics: GraphicsContext) -> None:
        self._rect = self._get_rect(graphics.screen)
        self._screen = graphics.screen
        self._input_component = graphics.input_component
        self._alert_component = graphics.alert_component
        self._time = time

    def render(self, screen_pos: Position) -> None:
        font = pygame.font.SysFont("Courier New", 24)
        rect = self._get_rect(self._screen)
        
        pygame.draw.rect(self._screen, Color.BLACK, rect)
        pygame.draw.rect(self._screen, Color.WHITE, rect, 2, border_radius=5)
        
        hours, minutes, secs = self._time.get_hms()

        def _format_part(p):
            if p == "--":
                return p
            return f"{int(p):02d}"

        hours_s = _format_part(hours)
        minutes_s = _format_part(minutes)
        secs_s = _format_part(secs)

        time_text = f"{hours_s}:{minutes_s}:{secs_s}"
        text_screen = font.render(time_text, True, Color.WHITE)
        rect = self._get_rect(self._screen)
        text_rect = text_screen.get_rect(center=rect.center)
        self._screen.blit(text_screen, text_rect)

    def _get_rect(self, screen: pygame.Surface) -> pygame.Rect:
        width, height = 130, 40
        x = (screen.get_width() - width) // 2
        y = 10
        return pygame.Rect(x, y, width, height)