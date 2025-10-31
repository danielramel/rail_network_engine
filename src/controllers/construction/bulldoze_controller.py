from controllers.construction.base_construction_controller import BaseConstructionController
from services.construction.bulldoze_target import BulldozeTargetType, find_bulldoze_target
from graphics.camera import Camera
from models.railway_system import RailwaySystem
from models.construction_state import ConstructionState
import pygame
from views.construction.bulldoze import BulldozeView

class BulldozeController(BaseConstructionController):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        view = BulldozeView(railway, state, camera, screen)
        super().__init__(view, railway, state, camera)
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.button == 3:
            self._construction_state.switch_mode(None)
            return True
        world_pos = self._camera.screen_to_world(event.screen_pos)
        target = find_bulldoze_target(self._railway, world_pos, self._camera.scale)
        if target.kind == BulldozeTargetType.SIGNAL:
            self._railway.signals.remove(target.pos)
            return True
        elif target.kind == BulldozeTargetType.STATION:
            self._railway.remove_station_at(target.pos)
            return True
        elif target.kind == BulldozeTargetType.PLATFORM:
            self._railway.remove_platform_at(target.edge)
            return True
        elif target.kind == BulldozeTargetType.SEGMENT:
            self._railway.graph.remove_segment_at(target.edge)
            return True
        return False