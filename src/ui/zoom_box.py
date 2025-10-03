import pygame
from models.geometry.position import Position
from ui.core.ui_element import UIElement
from config.colors import WHITE
from graphics.camera import Camera


class ZoomBox(UIElement):
    def __init__(self, surface: pygame.Surface, camera: Camera):
        self.rect = self._get_zoom_box(surface)
        self._camera = camera
        self._surface = surface

    def contains(self, pos: Position) -> bool:
        return self.rect.collidepoint(pos.x, pos.y)

    def draw(self) -> None:
        if self._camera.scale != 1.0 or self._camera.x != 0 or self._camera.y != 0:
            zoom_text = f"{int(self._camera.scale * 100)}%"
            zoom_font = pygame.font.SysFont(None, 24)
            zoom_surface = zoom_font.render(zoom_text, True, WHITE)
            zoom_box = self._get_zoom_box(self._surface)
            pygame.draw.rect(self._surface, (50, 50, 50), zoom_box, border_radius=4)
            pygame.draw.rect(self._surface, (150, 150, 150), zoom_box, 2, border_radius=4)
            self._surface.blit(zoom_surface, zoom_surface.get_rect(center=zoom_box.center))

    def _get_zoom_box(self, surface: pygame.Surface) -> pygame.Rect:
        return pygame.Rect(surface.get_width() - 100, 10, 80, 30)
    
    def handle_click(self, pos, *args):
        if self.contains(pos):
            self._camera.reset()
            return True
        return False