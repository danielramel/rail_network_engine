import pygame
from core.config.colors import BLACK
from core.config.settings import GRID_SIZE, TRAIN_LENGTH
from shared.controllers.mode_controller import ModeController
from core.models.railway.railway_system import RailwaySystem
from core.graphics.camera import Camera
from core.models.app_state import AppState
from shared.ui.models.ui_component import UIComponent
from shared.ui.components.load_button import LoadButton
from shared.ui.components.save_button import SaveButton
from shared.ui.components.mode_selector_buttons import ModeSelectorButtons

from shared.ui.components.timetable_button import TimeTableButton
from shared.ui.components.zoom_button import ZoomButton
from core.models.geometry import Position
from core.graphics.graphics_context import GraphicsContext
from shared.ui.models.ui_controller import UIController

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