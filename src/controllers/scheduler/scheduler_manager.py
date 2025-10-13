import pygame
from models.geometry import Position
    
from domain.rail_map import RailMap
from ui.components.base import BaseUIComponent
from views.scheduler.scheduler_view import SchedulerView


class SchedulerManager(BaseUIComponent):
    def __init__(self, map: RailMap, screen: pygame.Surface):
        self.view = SchedulerView(map, screen)
        self._map = map
        
    def handle_event(self, event):
        return True
            
    def render(self, screen_pos: Position | None):
        self.view.render(screen_pos)

    def contains(self, screen_pos: Position) -> bool:
        return True