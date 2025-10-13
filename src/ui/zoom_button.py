import pygame
from models.geometry.position import Position
from ui.components.rectangle import RectangleUIComponent
from config.colors import BLACK, WHITE
from graphics.camera import Camera


class ZoomButton(RectangleUIComponent):
    def __init__(self, surface: pygame.Surface, camera: Camera):
        self._camera = camera 
        self._rect = self._get_zoom_box(surface)
        self._surface = surface

    def render(self, screen_pos: Position) -> None:
        if self.is_hidden():
            return
        zoom_text = f"{int(self._camera.scale * 100)}%"
        zoom_font = pygame.font.SysFont(None, 24)
        zoom_surface = zoom_font.render(zoom_text, True, WHITE)
        zoom_box = self._get_zoom_box(self._surface)
        pygame.draw.rect(self._surface, BLACK, zoom_box, border_radius=4)
        pygame.draw.rect(self._surface, WHITE, zoom_box, 2, border_radius=4)
        self._surface.blit(zoom_surface, zoom_surface.get_rect(center=zoom_box.center))
        

    def _get_zoom_box(self, surface: pygame.Surface) -> pygame.Rect:
        return pygame.Rect(surface.get_width() - 100, 10, 80, 30)
    
    def handle_event(self, event: pygame.event) -> bool:
        if self.is_hidden():
            return False
        
        if self._rect.collidepoint(*event.pos_):
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._camera.reset()
            return True
        return False
    
    def contains(self, screen_pos):
        if self.is_hidden():
            return False
        return super().contains(screen_pos)
    
    
    def is_hidden(self) -> bool:
        return self._camera.is_reset()