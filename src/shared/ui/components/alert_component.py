from shared.ui.models.ui_component import UIComponent
import pygame
from core.models.event import Event
from core.config.color import Color

class AlertComponent(UIComponent):
    _visible: bool = False
    def __init__(self, screen: pygame.Surface):
        self._screen = screen
        
    def handle_event(self, event: Event):
        if not self._visible:
            return False
        
        if event.type == pygame.MOUSEBUTTONUP:
            self._visible = False
        if event.type == pygame.KEYDOWN:
            self._visible = False
            
        return True
            
    def alert(self, message: str):
        self._visible = True
        self._message = message
            
    def contains(self, screen_pos):
        return self._visible
    
    def render(self, screen_pos):
        if not self._visible:
            return

        w, h = self._screen.get_size()
        font = pygame.font.SysFont(None, 32)

        text_surf = font.render(self._message, True, Color.RED)
        text_rect = text_surf.get_rect(center=(w // 2, h // 2))

        padding_x = 60
        padding_y = 40
        box_rect = pygame.Rect(
            text_rect.x - padding_x,
            text_rect.y - padding_y,
            text_rect.width + padding_x * 2,
            text_rect.height + padding_y * 2
        )

        blur_src = self._screen.copy()
        small = pygame.transform.smoothscale(blur_src, (w // 10, h // 10))
        blur = pygame.transform.smoothscale(small, (w, h))
        blur.set_alpha(180)
        self._screen.blit(blur, (0, 0))

        pygame.draw.rect(self._screen, Color.BLACK, box_rect, border_radius=16)
        pygame.draw.rect(self._screen, Color.RED, box_rect, 2, border_radius=16)
        self._screen.blit(text_surf, text_rect)