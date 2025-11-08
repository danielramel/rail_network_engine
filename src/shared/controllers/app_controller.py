import pygame
from core.config.colors import BLACK
from shared.controllers.mode_controller import ModeController
from core.models.railway.railway_system import RailwaySystem
from core.graphics.camera import Camera
from core.models.app_state import AppState
from shared.ui.models.clickable_component import ClickComponent
from shared.ui.buttons.load_button import LoadButton
from shared.ui.buttons.save_button import SaveButton
from shared.ui.buttons.mode_selector_buttons import ModeSelectorButtons
from core.models.event import Event
from shared.ui.buttons.zoom_button import ZoomButton
from core.models.geometry import Position
from core.graphics.graphics_context import GraphicsContext
from shared.ui.models.ui_controller import UIController
from shared.ui.buttons.time_table_button import TimeTableButton

class AppController(UIController):
    def __init__(self, screen: pygame.Surface):
        self._graphics = GraphicsContext(screen, Camera())
        self._railway = RailwaySystem()
        self._app_state = AppState()
        self._last_mouse_down_pos: Position | None = None
        
        self._mock_load()
        
        self.elements: list[ClickComponent] = [
            TimeTableButton(screen, self._railway),
            ZoomButton(screen, self._graphics.camera),
            LoadButton(screen, self._railway),
            SaveButton(screen, self._railway),
            ModeSelectorButtons(screen, self._app_state),
            ModeController(self._app_state, self._railway, self._graphics)
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
        self._graphics.screen.fill(BLACK)
        screen_pos = Position(*pygame.mouse.get_pos())
        super().render(screen_pos)
            
            
    def _mock_load(self):
        import json
        filename = "C:/Users/lemar/elte/szakdolgozat/simulator/maps/cegléd.json"
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            self._railway.from_dict(data)