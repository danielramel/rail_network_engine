import pygame
from config.colors import BLACK
from config.settings import GRID_SIZE, PLATFORM_LENGTH, TRAIN_LENGTH
from controllers.construction.panel_strategy import ConstructionPanelStrategy
from models.railway_system import RailwaySystem
from graphics.camera import Camera
from models.app_state import AppState, ViewMode
from models.construction_state import ConstructionState
from models.simulation_state import SimulationState
from ui.models.base import UIComponent
from ui.components.load_button import LoadButton
from ui.components.save_button import SaveButton
from ui.components.mode_buttons import ModeSelectorButtons
from ui.simulation.time_control_buttons import TimeControlButtons
from ui.simulation.time_display import TimeDisplay
from ui.components.timetable_button import TimeTableButton
from ui.components.zoom_button import ZoomButton
from ui.construction.construction_buttons import ConstructionButtons
from controllers.construction.construction_controller import ConstructionController
from models.geometry import Position
from controllers.simulation.simulation_controller import SimulationController
from models.simulation_state import TimeControlState
from controllers.camera_controller import CameraController

class AppController:
    construction_element_types: dict[ViewMode, tuple[type]] = {
        ViewMode.CONSTRUCTION: (ConstructionButtons, ConstructionPanelStrategy, ConstructionController),
        ViewMode.SIMULATION: (TimeControlButtons, TimeDisplay, SimulationController),
    }
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.railway = RailwaySystem()
        self._mock_load()
        
        self.camera = Camera()
        self.app_state = AppState()
        self.construction_state = ConstructionState()
        self.simulation_state = SimulationState()
        
        self.elements: list[UIComponent] = [
            ModeSelectorButtons(screen, self.app_state),
            TimeTableButton(screen, self.railway),
            ZoomButton(screen, self.camera),
            LoadButton(screen, self.railway),
            SaveButton(screen, self.railway),
            CameraController(self.camera)
        ]
        
        self._add_mode_elements(self.app_state.mode)
    
    def _add_mode_elements(self, mode: ViewMode):
        """Create and add elements for the specified mode."""
        if mode == ViewMode.CONSTRUCTION:
            self.construction_state.reset()
            self.elements.extend([
                ConstructionButtons(self.screen, self.construction_state),
                SaveButton(self.screen, self.railway),
                LoadButton(self.screen, self.railway),
                ConstructionPanelStrategy(self.screen, self.construction_state),
                ConstructionController(self.railway, self.construction_state, self.camera, self.screen)
            ])
        elif mode == ViewMode.SIMULATION:
            self.simulation_state.time.reset()
            self._mock_load()
            self.elements.extend([
                TimeControlButtons(self.screen, self.simulation_state.time),
                TimeDisplay(self.screen, self.simulation_state.time),
                SimulationController(self.railway, self.camera, self.simulation_state, self.screen)
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

        event.screen_pos = Position(*pygame.mouse.get_pos())
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
                
    def tick(self):
        """Advance the simulation time if in simulation mode."""
        for element in self.elements:
            element.tick()
            
            
    def _mock_load(self):
        from models.train import Train
        from models.geometry.edge import Edge
        
        
        self.railway.stations.add(Position(100, 100), "Station A")
        self.railway.stations.add(Position(300, 100), "Station B")
        self.railway.stations.add(Position(500, 100), "Station C")
        self.railway.stations.add(Position(700, 100), "Station D")


        points = []
        for i in range(50):
            points.append(Position(80 + i * GRID_SIZE, 320))
            
        for i in range(50):
            points.append(Position(2080 + i * GRID_SIZE, 320 + i * GRID_SIZE))
            
        self.railway.graph.add_segment(points, 120)

        edges = [Edge(points[i+11], points[i + 12]) for i in range(TRAIN_LENGTH)]
        train = Train(-1, "Train 1", edges, self.railway)
        self.railway.trains.remove(-1)
        self.railway.trains.add(train)