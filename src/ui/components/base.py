import pygame

from models.geometry.position import Position

class BaseUIComponent:
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process a pygame event. Return True if consumed."""
        return False


    def render(self, world_pos: Position) -> None:
        """Render the UI component."""
        pass