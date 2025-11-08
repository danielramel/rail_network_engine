from shared.ui.models.ui_component import UIComponent
from core.models.geometry.position import Position

class FullScreenUIComponent(UIComponent):
    """A bottom UI component that takes the full width of the screen."""
    def contains(self, screen_pos: Position) -> bool:
        return True