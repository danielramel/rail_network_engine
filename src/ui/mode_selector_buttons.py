from ui.core.ui_element import UIElement
import pygame
from models.view import ViewMode


class ModeSelectorButtons(UIElement):
    def __init__(self, view_mode: ViewMode):
        self.buttons = self._get_buttons()
        self._view_mode = view_mode
        
    def contains(self, pos):
        return any(btn.collidepoint(pos.x, pos.y) for _, btn in self.buttons)
    
    def handle_event(self, pos) -> bool:
        return False  # Mode switching not implemented yet
    
    def render(self) -> None:
        pass
    
    @staticmethod
    def _get_buttons():
        return ((ViewMode.CONSTRUCTION, pygame.Rect(10, 10, 50, 50)),)
