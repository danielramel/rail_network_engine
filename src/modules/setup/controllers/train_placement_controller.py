import pygame
from core.models.geometry.position import Position
from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from modules.setup.view.train_placement_view import TrainPlacementView
from shared.ui.models.ui_component import UIComponent

class TrainPlacementController(UIComponent):
    handled_events = [pygame.MOUSEBUTTONUP]
    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext):
        self.view = TrainPlacementView(railway, graphics)
        
    def render(self, world_pos: Position) -> None:
        self.view.render(world_pos)
    
    def contains(self, screen_pos: Position) -> bool:
        return True