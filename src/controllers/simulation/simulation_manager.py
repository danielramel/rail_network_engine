import pygame
from models.geometry import Position
    
from graphics.camera import Camera
from domain.rail_map import RailMap
from models.event import Event, CLICK_TYPE
from ui.components.base import BaseUIComponent
from views.simulation.simulation_view import SimulationView


class SimulationManager(BaseUIComponent):
    def __init__(self, map: RailMap, camera: Camera, screen: pygame.Surface):
        self.view = SimulationView(map, camera, screen)
        self._map = map
        self._camera = camera

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._camera.start_drag(event.pos_)

        elif event.type == pygame.MOUSEMOTION:
            self._camera.update_drag(event.pos_)

        elif event.type == pygame.MOUSEWHEEL:
            self._camera.zoom(event.pos_, event.y)

        elif event.type == pygame.MOUSEBUTTONUP:
            was_dragging = self._camera.stop_drag(event.pos_)

            if was_dragging:
                return
            
            
            if event.button not in (1, 3):
                return
            
            click_type = CLICK_TYPE.LEFT_CLICK if event.button == 1 else CLICK_TYPE.RIGHT_CLICK
            event = Event(click_type, event.pos_)
            # handle click
            return True
            
            
    def render(self, screen_pos: Position | None):
        self.view.render(screen_pos)

    def contains(self, screen_pos: Position) -> bool:
        return True