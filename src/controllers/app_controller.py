import pygame
from config.colors import BLACK
from config.settings import GRID_SIZE, TRAIN_LENGTH
from controllers.mode_manager import ModeController
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
from ui.models.ui_handler import UILayer

class AppController(UILayer):    
    def __init__(self, screen: pygame.Surface):
        self.graphics = GraphicsContext(screen, Camera())
        self.railway = RailwaySystem()
        self.app_state = AppState()
        
        self.elements: list[UIComponent] = [
            ModeSelectorButtons(screen, self.app_state),
            TimeTableButton(screen, self.railway),
            ZoomButton(screen, self.graphics.camera),
            LoadButton(screen, self.railway),
            SaveButton(screen, self.railway),
            ModeController(self.app_state, self.railway, self.graphics)
        ]
    
    def handle_event(self, event: pygame.event):        
        if event.type == pygame.QUIT \
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return "quit"

        event.screen_pos = Position(*pygame.mouse.get_pos())
        super().handle_event(event)
    
    def render_view(self):
        self.graphics.screen.fill(BLACK)
        screen_pos = Position(*pygame.mouse.get_pos())
        super().render(screen_pos)
                
    def tick(self):
        """Advance the simulation time if in simulation mode."""
        for element in self.elements:
            element.tick()
            
            
    def _mock_load(self):
        return  # Disable mock load
        from models.train import Train
        from models.geometry.edge import Edge
        
        self.railway.stations._stations.clear()
        
        self.railway.stations.add(Position(80, 120), "Station A")
        self.railway.stations.add(Position(320, 120), "Station B")
        self.railway.stations.add(Position(520, 120), "Station C")
        self.railway.stations.add(Position(720, 120), "Station D")


        points: list[Position] = []
        for i in range(50):
            points.append(Position(80 + i * GRID_SIZE, 320))
            
        for i in range(50):
            points.append(Position(2080 + i * GRID_SIZE, 320 + i * GRID_SIZE))
            
        self.railway.graph.add_segment(points, 120)
        self.railway.signals.add(Pose(points[27], direction=points[27].direction_to(points[28])))
        self.railway.signals.add(Pose(points[37], direction=points[37].direction_to(points[38])))
        self.railway.signals.add(Pose(points[47], direction=points[47].direction_to(points[48])))

        edges = [Edge(points[i+11], points[i + 12]) for i in range(TRAIN_LENGTH)]
        train = Train(-1, "Train 1", edges, self.railway)
        self.railway.trains.remove(-1)
        self.railway.trains.add(train)