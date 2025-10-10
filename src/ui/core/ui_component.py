from abc import ABC, abstractmethod
import pygame

class BaseUIComponent(ABC):
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process a pygame event. Return True if consumed."""
        return False

    @abstractmethod
    def render(self) -> None:
        """Render the UI component."""
        pass