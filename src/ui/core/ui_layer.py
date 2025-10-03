from .ui_element import UIElement

class UILayer:
    """
    Manages a collection of UIElement instances and handles event routing.

    Elements are rendered and checked for clicks in the order they were added,
    with later elements appearing on top and receiving events first.
    """

    def __init__(self):
        self._elements: list[UIElement] = []

    def add(self, *elements: UIElement) -> None:
        """Add one or more UIElements to this layer."""
        self._elements.extend(elements)
        

    def remove(self, element: UIElement) -> None:
        """Remove a UIElement from this layer."""
        if element in self._elements:
            self._elements.remove(element)

    def clear(self) -> None:
        """Remove all UIElements from this layer."""
        self._elements.clear()

    def handle_click(self, pos) -> bool:
        """
        Handle a click event on this UI layer.

        Returns:
            True if any UIElement handled the event, False otherwise
        """
        for element in reversed(self._elements):
            if element.handle_click(pos):
                return True
        return False

    def is_over_ui(self, pos) -> bool:
        """Check if the position is over any UIElement."""
        for element in reversed(self._elements):
            if element.contains(pos):
                return True
        return False

    def draw(self) -> None:
        """Draw all UIElements in this layer."""
        for element in self._elements:
            if getattr(element, "visible", True):
                element.draw()
