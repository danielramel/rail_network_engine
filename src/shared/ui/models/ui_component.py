from core.models.geometry.position import Position
from core.models.event import Event
from abc import ABC, abstractmethod

class UIComponent(ABC):
    def dispatch_event(self, event: Event) -> bool:
        if hasattr(self, 'handled_events') and event.type not in self.handled_events:
            return False
        
        return self.handle_event(event)
    
    def handle_event(self, event: Event) -> bool:
        """Process an event that has already been filtered by type. Return True if consumed."""
        return False

    @abstractmethod
    def render(self, screen_pos: Position) -> None:
        """Render the UI component."""
        pass
    
    @abstractmethod
    def contains(self, screen_pos: Position) -> bool:
        """Check if a position is within the component's area."""
        return False
    
    def tick(self) -> None:
        """Advance the component's state by one tick."""
        pass