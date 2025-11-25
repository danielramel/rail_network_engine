import pygame
from core.config.color import Color
from core.config.settings import Config
from shared.controllers.mode_strategy import ModeStrategy
from core.models.railway.railway_system import RailwaySystem
from core.graphics.camera import Camera
from core.models.app_state import AppState, ViewMode
from shared.ui.components.exit_button import ExitButton
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
from typing import Callable

class AppController(UIController, FullScreenUIComponent):
    def __init__(self, screen: pygame.Surface, on_exit: Callable, filepath: str | None = None):
        self._railway = RailwaySystem()
        self._on_exit = on_exit
        self._app_state = AppState(filepath)
        alert_component = AlertComponent(screen)
        input_component = InputComponent(screen)
        if filepath is not None:
            successful = self.load_file(filepath)
            if not successful:
                alert_component.show_alert(f"Failed to load file: {filepath}\nCreating new empty simulation.")
            
                
        middle_position = self._railway.graph_service.get_graph_middle()
        w, h = screen.get_size()
        self._graphics = GraphicsContext(screen, Camera(middle_position, w, h), alert_component, input_component)
        self._last_mouse_down_pos: Position | None = None
        
        
        self.elements: list[ClickableUIComponent] = [
            alert_component,
            input_component,
            ExitButton(self._graphics, self._on_exit),
            RouteButton(screen, self._railway),
            ZoomButton(screen, self._graphics.camera),
            OpenButton(self._railway, self._app_state, self._graphics),
            SaveButton(screen, self._railway, self._app_state),
            ModeSelectorButtons(self._graphics, self._app_state),
            ModeStrategy(self._app_state, self._railway, self._graphics)
        ]
    
    def dispatch_event(self, pygame_event: pygame.event):
        try:
            screen_pos = Position(*pygame.mouse.get_pos())
            world_pos = self._graphics.camera.screen_to_world(screen_pos)
            event = Event(pygame_event, screen_pos, world_pos, self._last_mouse_down_pos)
            if pygame_event.type == pygame.MOUSEBUTTONDOWN:
                self._last_mouse_down_pos = screen_pos
            elif pygame_event.type == pygame.MOUSEBUTTONUP:
                self._last_mouse_down_pos = None
            
            
            super().dispatch_event(event)
        except Exception as e:
            print(f"Event dispatch error: {e}")
            print(f"Error type: {type(e).__name__}")
            print(f"Error details: {str(e)}")
            print(f"Traceback:")
            import traceback
            traceback.print_exc()
            print(f"Event type: {pygame_event.type if pygame_event else 'None'}")
            print(f"Screen position: {screen_pos if 'screen_pos' in locals() else 'Not set'}")
            print(f"World position: {world_pos if 'world_pos' in locals() else 'Not set'}")
            self._graphics.alert_component.show_alert(f"An unexpected error occurred during event handling:\n{e}")
    
    def render(self):
        try:
            self._graphics.screen.fill(Color.BLACK)
            screen_pos = Position(*pygame.mouse.get_pos())
            super().render(screen_pos)
        except Exception as e:
            print(f"Render error: {e}")
            self._graphics.alert_component.show_alert(f"An unexpected error occurred during rendering:\n{e}")
            
    def load_file(self, filepath: str) -> None:
        import json
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())
                self._railway.replace_from_dict(data)
                return True
        except Exception as e:
            return False    
