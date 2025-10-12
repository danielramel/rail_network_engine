import pygame

from config.colors import BLACK
from domain.rail_map import RailMap
from graphics.camera import Camera
from models.app_state import AppState
from models.construction import ConstructionState
from ui.components.base import BaseUIComponent
from ui.mode_buttons import ModeSelectorButtons
from ui.zoom_box import ZoomBox
from ui.construction.construction_buttons import ConstructionButtons
from controllers.construction.construction_manager import ConstructionManager
from models.geometry import Position


class AppController:
    ACCEPTED_EVENTS = [
        pygame.QUIT,
        pygame.KEYDOWN,
        pygame.MOUSEBUTTONDOWN,
        pygame.MOUSEBUTTONUP,
        pygame.MOUSEMOTION,
        pygame.MOUSEWHEEL
    ]

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.map = RailMap()
        self.camera = Camera()
        self.state = AppState()
        
        self.construction_state = ConstructionState()
        self.elements : list[BaseUIComponent] = [
            ModeSelectorButtons(screen, self.state),
            ZoomBox(screen, self.camera),
            ConstructionButtons(screen, self.construction_state),
            ConstructionManager(self.map, self.construction_state, self.camera, screen)
        ]
         
        
    def handle_event(self, event: pygame.event):
        if event.type == pygame.QUIT\
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return "quit"
        
        if event.type not in self.ACCEPTED_EVENTS:
            return
        
        event.pos_ = Position(*pygame.mouse.get_pos())

        for element in self.elements:
            if hasattr(element, "handled_events") and event.type not in element.handled_events:
                continue
            action = element.handle_event(event)
            if action:
                break #mode switch
            
    def render_view(self):
        self.screen.fill(BLACK)
        pos = Position(*pygame.mouse.get_pos())
        elements_above_cursor = []
        for element in self.elements:
            elements_above_cursor.append(element)
            if element.contains(pos):
                break
                
        for element in reversed(self.elements):
            if element in elements_above_cursor:
                element.render(pos)
            else:
                element.render(None)
            