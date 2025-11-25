from shared.ui.models.ui_component import UIComponent
import pygame
from core.models.event import Event
from core.config.color import Color

class AlertComponent(UIComponent):
    _visible: bool = False
    def __init__(self, screen: pygame.Surface):
        self._screen = screen
        
        self._font = pygame.font.SysFont(None, 32)
        self._padding_x = 60
        self._padding_y = 40
        
    def handle_event(self, event: Event):
        if not self._visible:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key not in (pygame.K_RETURN, pygame.K_ESCAPE):
                return False
            self._visible = False
            return True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._visible = False
            return True
            
    def show_alert(self, message: str):
        self._visible = True
        self._message = message
        
        # Precompute box_rect and related elements
        w, h = self._screen.get_size()
        self._text_surf = self._font.render(self._message, True, Color.RED)
        self._text_rect = self._text_surf.get_rect(center=(w // 2, h // 2))
        
        self._box_rect = pygame.Rect(
            self._text_rect.x - self._padding_x,
            self._text_rect.y - self._padding_y,
            self._text_rect.width + self._padding_x * 2,
            self._text_rect.height + self._padding_y * 2
        )
            
    def contains(self, screen_pos):
        return self._visible
    
    def render(self, screen_pos):
        if not self._visible:
            return

        w, h = self._screen.get_size()
        
        blur_src = self._screen.copy()
        small = pygame.transform.smoothscale(blur_src, (w // 10, h // 10))
        blur = pygame.transform.smoothscale(small, (w, h))
        blur.set_alpha(180)
        self._screen.blit(blur, (0, 0))

        pygame.draw.rect(self._screen, Color.BLACK, self._box_rect, border_radius=16)
        pygame.draw.rect(self._screen, Color.RED, self._box_rect, 2, border_radius=16)
        self._screen.blit(self._text_surf, self._text_rect)