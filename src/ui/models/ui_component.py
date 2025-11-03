import pygame

from models.geometry.position import Position

class UIComponent:
    def dispatch_event(self, event: pygame.event.Event) -> bool:
        """Process a pygame event. Return True if consumed."""
        if hasattr(self, 'handled_events') and event.type not in self.handled_events:
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