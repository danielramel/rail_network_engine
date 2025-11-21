import pygame
from core.models.event import Event
from core.models.geometry.position import Position
from shared.ui.models.rectangle import RectangleUIComponent
from shared.ui.models.clickable_ui_component import ClickableUIComponent

from core.config.color import Color
from core.graphics.camera import Camera


class ZoomButton(RectangleUIComponent, ClickableUIComponent):
    def __init__(self, screen: pygame.Surface, camera: Camera):
        self._camera = camera 
        self._rect = self._get_zoom_box(screen)
        self._screen = screen

    def render(self, screen_pos: Position) -> None:
        if self.is_hidden():
            return
        zoom_text = f"{int(self._camera.scale * 100)}%"
        zoom_font = pygame.font.SysFont(None, 24)
        zoom_screen = zoom_font.render(zoom_text, True, Color.WHITE)
        zoom_box = self._get_zoom_box(self._screen)
        pygame.draw.rect(self._screen, Color.BLACK, zoom_box, border_radius=4)
        pygame.draw.rect(self._screen, Color.WHITE, zoom_box, 2, border_radius=4)
        self._screen.blit(zoom_screen, zoom_screen.get_rect(center=zoom_box.center))
        

    def _get_zoom_box(self, screen: pygame.Surface) -> pygame.Rect:
        w, h = screen.get_size()
        return pygame.Rect(w - 100, h - 50, 80, 30)
    
    def _on_click(self, event: Event) -> bool:        
        if event.is_left_click:
            self._camera.reset()
    
    def contains(self, screen_pos):
        if self.is_hidden():
            return False
        return super().contains(screen_pos)
    
    
    def is_hidden(self) -> bool:
        return self._camera.is_reset()