from controllers.construction.base_construction_controller import BaseConstructionController
from services.construction.bulldoze_target import BulldozeTargetType, find_bulldoze_target
from models.event import CLICK_TYPE, Event
from graphics.camera import Camera
from models.simulation import Simulation
from models.construction import ConstructionState
import pygame
from views.construction.bulldoze import BulldozeView

class BulldozeController(BaseConstructionController):
    def __init__(self, map: Simulation, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        view = BulldozeView(map, state, camera, screen)
        super().__init__(view, map, state, camera)
        
    def handle_event(self, event: Event):
        if event.click_type == CLICK_TYPE.RIGHT_CLICK:
            self._construction_state.switch_mode(None)
            return
        world_pos = self._camera.screen_to_world(event.screen_pos)
        target = find_bulldoze_target(self._simulation, world_pos, self._camera.scale)
        if target.kind == BulldozeTargetType.SIGNAL:
            self._simulation.signals.remove(target.pos)
            return True
        elif target.kind == BulldozeTargetType.STATION:
            self._simulation.remove_station_at(target.pos)
            return True
        elif target.kind == BulldozeTargetType.PLATFORM:
            self._simulation.remove_platform_at(target.edge)
            return True
        elif target.kind == BulldozeTargetType.SEGMENT:
            self._simulation.graph.remove_segment_at(target.edge)
            return True
        return False