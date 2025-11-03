import pygame
from ui.models.ui_component import UIComponent

class UILayer(UIComponent):
    elements: tuple[UIComponent]
    
    def handle_event(self, event):
        for element in self.elements:
            if element.handle_event(event):
                return True
            
        return False
    
    def render(self, screen_pos):
        elements_above_cursor = []
        if screen_pos is not None:
            for element in self.elements:
                elements_above_cursor.append(element)
                if element.contains(screen_pos):
                    break

        for element in reversed(self.elements):
            if element in elements_above_cursor:
                element.render(screen_pos)
            else:
                element.render(None)