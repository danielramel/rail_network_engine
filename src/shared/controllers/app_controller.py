import pygame
from core.config.color import Color
from core.config.settings import Config
from shared.controllers.mode_strategy import ModeStrategy
from core.models.railway.railway_system import RailwaySystem
from core.graphics.camera import Camera
from core.models.app_state import AppState
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.components.open_button import OpenButton
from shared.ui.components.save_button import SaveButton
from shared.ui.components.mode_selector_buttons import ModeSelectorButtons
from core.models.event import Event
from shared.ui.components.zoom_button import ZoomButton
from core.models.geometry.position import Position
from core.graphics.graphics_context import GraphicsContext
from shared.ui.models.ui_controller import UIController
from shared.ui.components.route_button import RouteButton
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from shared.ui.components.alert_component import AlertComponent
from shared.ui.components.input_component import InputComponent

class AppController(UIController, FullScreenUIComponent):
    def __init__(self, screen: pygame.Surface):
        self._railway = RailwaySystem()
        filename = self.load_file()
        self._app_state = AppState(filename)
        alert_component = AlertComponent(screen)
        input_component = InputComponent(screen)
        middle_position = self._railway.graph_service.get_graph_middle()
        w, h = screen.get_size()
        self._graphics = GraphicsContext(screen, Camera(middle_position, w, h), alert_component, input_component)
        self._last_mouse_down_pos: Position | None = None
        
        
        self.elements: list[ClickableUIComponent] = [
            alert_component,
            input_component,
            RouteButton(screen, self._railway),
            ZoomButton(screen, self._graphics.camera),
            OpenButton(screen, self._railway, self._app_state),
            SaveButton(screen, self._railway, self._app_state),
            ModeSelectorButtons(self._graphics, self._app_state),
            ModeStrategy(self._app_state, self._railway, self._graphics)
        ]
    
    def dispatch_event(self, pygame_event: pygame.event):        
        if pygame_event.type == pygame.QUIT \
            or (pygame_event.type == pygame.KEYDOWN and pygame_event.key == pygame.K_ESCAPE):
            return "quit"


        screen_pos = Position(*pygame.mouse.get_pos())
        world_pos = self._graphics.camera.screen_to_world(screen_pos)
        event = Event(pygame_event, screen_pos, world_pos, self._last_mouse_down_pos)
        if pygame_event.type == pygame.MOUSEBUTTONDOWN:
            self._last_mouse_down_pos = screen_pos
        elif pygame_event.type == pygame.MOUSEBUTTONUP:
            self._last_mouse_down_pos = None
        
        
        super().dispatch_event(event)
    
    def render(self):
        self._graphics.screen.fill(Color.BLACK)
        screen_pos = Position(*pygame.mouse.get_pos())
        super().render(screen_pos)
            
            
    def load_file(self):
        import sys
        import json
        if len(sys.argv) < 2:
            return None
        filename = sys.argv[1]
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            self._railway.replace_from_dict(data)
            
        return filename
    
    
    
    
    
    
    
    
# #TODO create main menu
# enter exit from map
# ask for save on exit
# create camera centering method