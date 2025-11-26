from shared.ui.models.ui_component import UIComponent
import pygame
from core.models.event import Event
from core.config.color import Color
from typing import Callable

class InputComponent(UIComponent):
    _visible: bool = False
    _hint: str = ""
    _input_text: str = ""
    _callback: Callable | None = None

    def __init__(self, screen: pygame.Surface):
        self._screen = screen
        self._box_rect = pygame.Rect(0, 0, 0, 0)

    def handle_event(self, event: Event):
        if not self._visible:
            return False
        
        if event.type == pygame.MOUSEBUTTONUP and not self._box_rect.collidepoint(*event.screen_pos):
            self._visible = False
            self._callback(None)
            return True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._visible = False
                self._callback(self._input_text)
                return True

            elif event.key == pygame.K_ESCAPE:
                self._visible = False
                self._callback(None)
                return True
            
            elif event.key == pygame.K_BACKSPACE:
                self._input_text = self._input_text[:-1]
                return True
            
                
            char = event.unicode
            if char.isprintable():
                self._input_text += char
                return True
        return True

    def request_input(self, hint: str, callback: Callable):
        self._visible = True
        self._hint = hint
        self._input_text = ""
        self._callback = callback

    def contains(self, screen_pos):
        return self._visible

    def render(self, screen_pos):
        if not self._visible:
            return

        w, h = self._screen.get_size()
        font = pygame.font.SysFont(None, 32)

        # Calculate hint size for minimum box dimensions
        hint_surf = font.render(self._hint, True, Color.GREY)
        hint_rect = hint_surf.get_rect()
        min_box_w = hint_rect.width + 60
        min_box_h = hint_rect.height + 60

        # Show either hint or input text
        if len(self._input_text) == 0:
            text_surf = hint_surf
        else:
            text_surf = font.render(self._input_text, True, Color.WHITE)
            
        text_rect = text_surf.get_rect(center=(w // 2, h // 2))

        box_w = max(text_rect.width + 60, min_box_w)
        box_h = max(text_rect.height + 60, min_box_h)
        self._box_rect = pygame.Rect(
            (w - box_w) // 2,
            (h - box_h) // 2,
            box_w,
            box_h
        )

        blur_src = self._screen.copy()
        small = pygame.transform.smoothscale(blur_src, (w // 10, h // 10))
        blur = pygame.transform.smoothscale(small, (w, h))
        blur.set_alpha(130)
        self._screen.blit(blur, (0, 0))

        pygame.draw.rect(self._screen, Color.BLACK, self._box_rect, border_radius=16)
        pygame.draw.rect(self._screen, Color.BLUE, self._box_rect, 2, border_radius=16)

        self._screen.blit(text_surf, text_rect)
