import pygame
from config.colors import BLACK
from config.settings import GRID_SIZE, TRAIN_LENGTH
from controllers.mode_controller import ModeController
from models.geometry.pose import Pose
from models.railway_system import RailwaySystem
from graphics.camera import Camera
from models.app_state import AppState
from ui.models.ui_component import UIComponent
from ui.components.load_button import LoadButton
from ui.components.save_button import SaveButton
from ui.components.mode_selector_buttons import ModeSelectorButtons

from ui.components.timetable_button import TimeTableButton
from ui.components.zoom_button import ZoomButton
from models.geometry import Position
from graphics.graphics_context import GraphicsContext
from ui.models.ui_controller import UIController

class AppController(UIController):
    def __init__(self, screen: pygame.Surface):
        self._graphics = GraphicsContext(screen, Camera())
        self._railway = RailwaySystem()
        self._app_state = AppState()
        
        self._mock_load()
        
        self.elements: list[UIComponent] = [
            TimeTableButton(screen, self._railway),
            ZoomButton(screen, self._graphics.camera),
            LoadButton(screen, self._railway),
            SaveButton(screen, self._railway),
            ModeSelectorButtons(screen, self._app_state),
            ModeController(self._app_state, self._railway, self._graphics)
        ]
    
    def dispatch_event(self, event: pygame.event):        
        if event.type == pygame.QUIT \
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return "quit"

        event.screen_pos = Position(*pygame.mouse.get_pos())
        super().dispatch_event(event)
    
    def render(self):
        self._graphics.screen.fill(BLACK)
        screen_pos = Position(*pygame.mouse.get_pos())
        super().render(screen_pos)
            
            
    def _mock_load(self):
        import json
        
        filename = "C:/Users/lemar/elte/szakdolgozat/simulator/maps/cegléd.json"
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            self._railway.from_dict(data)