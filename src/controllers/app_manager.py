import pygame
from config.colors import BLACK
from controllers.construction.panel_strategy import ConstructionPanelStrategy
from domain.rail_map import RailMap
from graphics.camera import Camera
from models.app_state import AppState, ViewMode
from models.construction import ConstructionState
from ui.components.base import BaseUIComponent
from ui.mode_buttons import ModeSelectorButtons
from ui.simulation.time_control_buttons import TimeControlButtons
from ui.simulation.time_display import TimeDisplay
from ui.zoom_box import ZoomButton
from ui.construction.construction_buttons import ConstructionButtons
from controllers.construction.construction_manager import ConstructionManager
from models.geometry import Position
from controllers.simulation.simulation_manager import SimulationManager
from models.time import TimeControlState

class AppController:
    construction_element_types: dict[ViewMode, tuple[type]] = {
        ViewMode.CONSTRUCTION: (ConstructionButtons, ConstructionPanelStrategy, ConstructionManager),
        ViewMode.SIMULATION: (TimeControlButtons, TimeDisplay, SimulationManager)
    }
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.map = RailMap()
        self.camera = Camera()
        self.app_state = AppState()
        self.construction_state = ConstructionState()
        self.time_control_state = TimeControlState()
        
        
        self.elements: list[BaseUIComponent] = [
            ModeSelectorButtons(screen, self.app_state),
            ZoomButton(screen, self.camera),
        ]
        
        self._add_mode_elements(self.app_state.mode)
    
    def _add_mode_elements(self, mode: ViewMode):
        """Create and add elements for the specified mode."""
        if mode == ViewMode.CONSTRUCTION:
            self.construction_state.reset()
            self.elements.extend([
                ConstructionButtons(self.screen, self.construction_state),
                ConstructionPanelStrategy(self.screen, self.construction_state),
                ConstructionManager(self.map, self.construction_state, self.camera, self.screen)
            ])
        elif mode == ViewMode.SIMULATION:
            self.time_control_state.reset()
            self.elements.extend([
                TimeControlButtons(self.screen, self.time_control_state),
                TimeDisplay(self.screen, self.time_control_state),
                SimulationManager(self.map, self.camera, self.screen)
            ])
        # Add other modes as needed
    
    def _remove_mode_elements(self, mode: ViewMode):
        """Remove elements specific to the given mode."""
        element_types = self.construction_element_types[mode]
        self.elements = [e for e in self.elements if not isinstance(e, element_types)]
    
    def handle_event(self, event: pygame.event):
        old_app_mode = self.app_state.mode
        
        if event.type == pygame.QUIT \
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return "quit"

        event.pos_ = Position(*pygame.mouse.get_pos())
        for element in self.elements:
            if hasattr(element, "handled_events") and event.type not in element.handled_events:
                continue
            handled = element.handle_event(event)
            if handled:
                break
        
        # Handle mode change
        if old_app_mode != self.app_state.mode:
            self._remove_mode_elements(old_app_mode)
            self._add_mode_elements(self.app_state.mode)
    
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