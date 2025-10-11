from models.construction import EdgeType
from views.construction.base_construction_view import BaseConstructionView
from models.geometry import Position
from config.colors import PURPLE, LIGHTBLUE
from ui.utils import draw_node, draw_station, draw_dotted_line
from services.construction.platform_target import PlatformTargetType, find_platform_target

class PlatformView(BaseConstructionView):
    def render(self, world_pos: Position):
        # handle the “select_station” preview mode first
        if self._construction_state.platform_waiting_for_station:
            middle_point = self._map.get_middle_of_platform(self._construction_state.preview_edges)
            for station_pos in self._map.station_positions:
                if world_pos.is_within_station_rect(station_pos):
                    draw_station(self._surface, self._map.get_station_at(station_pos), self._camera, color=LIGHTBLUE)
                    draw_dotted_line(self._surface, station_pos, middle_point, self._camera, color=LIGHTBLUE)
                    break
            else:
                draw_dotted_line(self._surface, world_pos, middle_point, self._camera, color=LIGHTBLUE)
            return

        # reset preview edges/state
        self._construction_state.preview_edges = frozenset()
        self._construction_state.preview_edges_type = None

        # handle the platform target preview
        target = find_platform_target(self._map, world_pos, self._camera.scale)
        if target.kind in (PlatformTargetType.NONE, PlatformTargetType.EXISTING_PLATFORM):
            draw_node(self._surface, world_pos, self._camera, color=PURPLE)
            return

        self._construction_state.preview_edges = target.edges
        self._construction_state.preview_edges_type = EdgeType.PLATFORM if target.is_valid else EdgeType.INVALID_PLATFORM