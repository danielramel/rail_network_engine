import pygame

class BaseUIComponent:
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process a pygame event. Return True if consumed."""
        return False


    def render(self) -> None:
        """Render the UI component."""
        pass