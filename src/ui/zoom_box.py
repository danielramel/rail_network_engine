import pygame
from models.geometry.position import Position
from ui.components.rectangle import RectangleUIComponent
from config.colors import WHITE
from graphics.camera import Camera


class ZoomBox(RectangleUIComponent):
    def __init__(self, surface: pygame.Surface, camera: Camera):
        self._rect = self._get_zoom_box(surface)
        self._camera = camera 
        self._surface = surface

    def render(self, screen_pos: Position) -> None:
        if not self.is_visible:
            return
        zoom_text = f"{int(self._camera.scale * 100)}%"
        zoom_font = pygame.font.SysFont(None, 24)
        zoom_surface = zoom_font.render(zoom_text, True, WHITE)
        zoom_box = self._get_zoom_box(self._surface)
        pygame.draw.rect(self._surface, (50, 50, 50), zoom_box, border_radius=4)
        pygame.draw.rect(self._surface, (150, 150, 150), zoom_box, 2, border_radius=4)
        self._surface.blit(zoom_surface, zoom_surface.get_rect(center=zoom_box.center))
        
    @property
    def is_visible(self) -> bool:
        return not self._camera.is_reset()

    def _get_zoom_box(self, surface: pygame.Surface) -> pygame.Rect:
        return pygame.Rect(surface.get_width() - 100, 10, 80, 30)
    
    def handle_event(self, event: pygame.event) -> bool:
        pos = Position(*event.pos)
        if self._rect.collidepoint(*pos):
            self._camera.reset()
            return True
        return False