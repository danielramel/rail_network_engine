import pygame
from core.models.event import Event
from shared.ui.models.ui_component import UIComponent

class ClickableUIComponent(UIComponent):
    handled_events = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL]
    """A UI component that only processes click-related events."""
    def handle_event(self, event: Event) -> bool:
        """Process a pygame event. Return True if consumed."""
        if event.is_far_click:
            return False
        
        if self.contains(event.screen_pos):
            if event.type == pygame.MOUSEBUTTONUP:
                self._on_click(event)
            return True
            
        return False
    
    def _on_click(self, event: Event) -> bool:
        pass