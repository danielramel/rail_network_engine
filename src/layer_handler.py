import pygame

from config.colors import BLACK
from domain.rail_map import RailMap
from graphics.camera import Camera
from models.construction import ConstructionState
from ui.zoom_box import ZoomBox
from ui.construction.construction_buttons import ConstructionButtons
from controllers.construction.construction import ConstructionController


class LayerHandler:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.map = RailMap()
        self.camera = Camera()
        
        self.construction_state = ConstructionState()
        self.elements = [
            ZoomBox(screen, self.camera),
            ConstructionButtons(screen, self.construction_state),
            ConstructionController(self.map, self.construction_state, self.camera, screen)
        ]
        
        
        
    def handle_event(self, event: pygame.event):
        if event.type == pygame.QUIT\
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return "quit"
        
        for element in self.elements:
            if hasattr(element, "handled_events") and event.type not in element.handled_events:
                continue
            action = element.handle_event(event)
            if action:
                break #mode switch
            
    def render_view(self):
        self.screen.fill(BLACK)
        for element in reversed(self.elements):
            element.render()