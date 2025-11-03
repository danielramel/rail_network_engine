import pygame
from controllers.construction.base_construction_controller import BaseConstructionController
from models.geometry.direction import Direction
from services.construction.rail_target import find_rail_target, RailTargetType
from models.geometry import Pose
from views.construction.rail_view import RailView
from graphics.graphics_context import GraphicsContext
from models.railway_system import RailwaySystem
from models.construction_state import ConstructionState

class RailController(BaseConstructionController):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        view = RailView(railway, state, graphics)
        super().__init__(view, railway, state, graphics.camera)
        
        
    def process_event(self, event: pygame.event.Event) -> None:
        if event.button == 3:
            if self._construction_state.construction_anchor is not None:
                self._construction_state.construction_anchor = None
            else:
                self._construction_state.switch_mode(None)
            return
        
        target = find_rail_target(self._railway, self._camera.screen_to_world(event.screen_pos), self._construction_state.construction_anchor)

        if target.kind == RailTargetType.NODE:
            self._construction_state.construction_anchor = Pose(target.snapped, Direction(0, 0))

        elif target.kind == RailTargetType.ANCHOR_SAME:
            self._construction_state.construction_anchor = None


        elif target.kind == RailTargetType.PATH:
            self._railway.graph_service.add_segment(target.found_path, self._construction_state.track_speed)
            self._construction_state.construction_anchor = Pose(
                target.snapped,
                target.found_path[-2].direction_to(target.snapped)
            )
