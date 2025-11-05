import pygame
from modules.construction.controllers.base_construction_tool_controller import BaseConstructionToolController
from core.models.geometry.direction import Direction
from modules.construction.services.rail_target import find_rail_target, RailTargetType
from core.models.geometry import Pose
from modules.construction.views.rail_view import RailView
from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from modules.construction.construction_state import ConstructionState

class RailController(BaseConstructionToolController):
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
            self._railway.graph_service.add_segment(target.found_path, self._construction_state.track_speed, self._construction_state.track_length)
            self._construction_state.construction_anchor = Pose(
                target.snapped,
                target.found_path[-2].direction_to(target.snapped)
            )
