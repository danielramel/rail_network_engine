from shared.ui.models.ui_component import UIComponent
from core.models.event import Event

class UIController(UIComponent):
    elements: tuple[UIComponent]
    
    def dispatch_event(self, event: Event):
        for element in self.elements:
            if element.dispatch_event(event):
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
                
    def tick(self):
        for element in self.elements:
            element.tick()
            
    def contains(self, screen_pos):
        return any(element.contains(screen_pos) for element in self.elements)