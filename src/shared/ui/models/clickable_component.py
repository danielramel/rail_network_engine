from core.models.event import Event
from shared.ui.models.ui_component import UIComponent

class ClickableComponent(UIComponent):
    def dispatch_event(self, event: Event) -> bool:
        """Process a pygame event. Return True if consumed."""
        if event.is_far_click:
            return False
        
        return super().dispatch_event(event)