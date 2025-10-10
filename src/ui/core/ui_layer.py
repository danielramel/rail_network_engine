"""import pygame
from controllers.ui_controller import UIController
from .ui_element import UIElement

class UILayer(UIElement):
    def __init__(self, controllers: list[UIController] = None) -> None:
        self._controllers: list[UIController] = controllers if controllers is not None else []

    def add(self, *controllers: UIController) -> None:
        self._controllers.extend(controllers)

    def remove(self, controller: UIController) -> None:
        if controller in self._controllers:
            self._controllers.remove(controller)

    def clear(self) -> None:
        self._controllers.clear()

    def handle_event(self, event: pygame.event.Event) -> bool:
        # dispatch top-most first (reverse order)
        for c in reversed(self._controllers):
            if c.handle_event(event):
                return

    def render(self, surface: pygame.Surface, **ctx) -> None:
        # drawing in insertion order so earlier controllers appear underneath
        for c in self._controllers:
            c.render(surface, **ctx)
"""