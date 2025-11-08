import pygame
from core.models.railway.railway_system import RailwaySystem
from modules.construction.models.construction_state import ConstructionState
from core.graphics.graphics_context import GraphicsContext
from modules.construction.controllers.tools.construction_tool_controller import ConstructionToolController
from modules.construction.views.bulldoze_view import BulldozeView
from modules.construction.services.bulldoze_target import BulldozeTargetType, find_bulldoze_target
from core.models.event import Event

class BulldozeController(ConstructionToolController):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, graphics: GraphicsContext):
        view = BulldozeView(railway, state, graphics)
        super().__init__(view, railway, state, graphics.camera)

    def process_event(self, event: Event) -> bool:
        if event.button == 3:
            self._construction_state.switch_mode(None)
            return True
        world_pos = self._camera.screen_to_world(event.screen_pos)
        target = find_bulldoze_target(self._railway, world_pos, self._camera.scale)
        if target.kind == BulldozeTargetType.SIGNAL:
            self._railway.signals.remove(target.position)
            return True
        elif target.kind == BulldozeTargetType.STATION:
            self._railway.stations.remove_station_at(target.position)
            return True
        elif target.kind == BulldozeTargetType.PLATFORM:
            self._railway.stations.remove_platform_at(target.edge)
            return True
        elif target.kind == BulldozeTargetType.SEGMENT:
            self._railway.graph_service.remove_segment(target.nodes, target.edges)
            return True
        return False