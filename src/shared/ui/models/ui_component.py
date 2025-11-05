import pygame

from core.models.geometry.position import Position

class UIComponent:
    def dispatch_event(self, event: pygame.event.Event, mouse_event_filter: bool = True) -> bool:
        """Process a pygame event. Return True if consumed."""
        if hasattr(self, 'handled_events') and event.type not in self.handled_events:
            return False
        if event.type == pygame.MOUSEBUTTONUP and event.button not in (1, 3) and mouse_event_filter:
            return False
        
        return self.process_event(event)
    
    def process_event(self, event: pygame.event.Event) -> bool:
        """Process a pygame event that has already been filtered by type. Return True if consumed."""
        return False


    def render(self, screen_pos: Position) -> None:
        """Render the UI component."""
        pass
    
    def contains(self, screen_pos: Position) -> bool:
        """Check if a position is within the component's area."""
        return False
    
    def tick(self) -> None:
        """Advance the component's state by one tick."""
        pass