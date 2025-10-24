import pygame
from config.colors import BLACK
from controllers.construction.panel_strategy import ConstructionPanelStrategy
from models.simulation import Simulation
from graphics.camera import Camera
from models.app_state import AppState, ViewMode
from models.construction import ConstructionState
from ui.models.base import UIComponent
from ui.components.load_button import LoadButton
from ui.components.save_button import SaveButton
from ui.components.mode_buttons import ModeSelectorButtons
from ui.simulation.time_control_buttons import TimeControlButtons
from ui.simulation.time_display import TimeDisplay
from ui.components.timetable_button import TimeTableButton
from ui.components.zoom_button import ZoomButton
from ui.construction.construction_buttons import ConstructionButtons
from controllers.construction.construction_manager import ConstructionController
from models.geometry import Position
from controllers.simulation.simulation_manager import SimulationManager
from models.time import TimeControlState

class AppController:
    construction_element_types: dict[ViewMode, tuple[type]] = {
        ViewMode.CONSTRUCTION: (ConstructionButtons, SaveButton, LoadButton, ConstructionPanelStrategy, ConstructionController),
        ViewMode.SIMULATION: (TimeControlButtons, TimeDisplay, SimulationManager),
    }
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.simulation = Simulation()
        # mockup
        self.simulation.stations.add(Position(100, 100), "Station A")
        self.simulation.stations.add(Position(300, 100), "Station B")
        self.simulation.stations.add(Position(500, 100), "Station C")
        self.simulation.stations.add(Position(700, 100), "Station D")
        self.simulation.stations.add(Position(100, 300), "Station E")
        self.simulation.stations.add(Position(300, 300), "Station F")
        self.simulation.stations.add(Position(500, 300), "Station G")
        self.simulation.stations.add(Position(700, 300), "Station H")
        self.simulation.stations.add(Position(100, 500), "Station I")
        self.simulation.stations.add(Position(300, 500), "Station J")
        self.simulation.stations.add(Position(500, 500), "Station K")
        self.simulation.stations.add(Position(700, 500), "Station L")
        self.simulation.stations.add(Position(900, 100), "Station M")
        self.simulation.stations.add(Position(900, 300), "Station N")
        
        # mockup end
        self.camera = Camera()
        self.app_state = AppState()
        self.construction_state = ConstructionState()
        self.time_control_state = TimeControlState()
        
        self.elements: list[UIComponent] = [
            ModeSelectorButtons(screen, self.app_state),
            TimeTableButton(screen, self.simulation),
            ZoomButton(screen, self.camera),
        ]
        
        self._add_mode_elements(self.app_state.mode)
    
    def _add_mode_elements(self, mode: ViewMode):
        """Create and add elements for the specified mode."""
        if mode == ViewMode.CONSTRUCTION:
            self.construction_state.reset()
            self.elements.extend([
                ConstructionButtons(self.screen, self.construction_state),
                SaveButton(self.screen, self.simulation),
                LoadButton(self.screen, self.simulation),
                ConstructionPanelStrategy(self.screen, self.construction_state),
                ConstructionController(self.simulation, self.construction_state, self.camera, self.screen)
            ])
        elif mode == ViewMode.SIMULATION:
            self.time_control_state.reset()
            self.elements.extend([
                TimeControlButtons(self.screen, self.time_control_state),
                TimeDisplay(self.screen, self.time_control_state),
                SimulationManager(self.simulation, self.camera, self.screen)
            ])
    
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