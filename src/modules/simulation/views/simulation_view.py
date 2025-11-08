from core.config.colors import BLUE, GREEN, LIME, RED, WHITE, LIGHTBLUE, YELLOW
from shared.ui.models.clickable_component import ClickableComponent
from shared.ui.utils import draw_track, draw_node, draw_signal, draw_station, draw_occupied_edge
from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from modules.simulation.models.simulation_state import SimulationState
from shared.ui.enums.edge_action import EdgeAction
from core.models.geometry.position import Position


class SimulationView(ClickableComponent):
    def __init__(self, railway: RailwaySystem, simulation_state: SimulationState, graphics: GraphicsContext):
        self._railway = railway
        self._state = simulation_state
        self._surface = graphics.screen
        self._camera = graphics.camera
        
    def render(self, world_pos: Position | None) -> None:
        # draw_grid(self._surface, self._camera)
        self.set_preview(world_pos)

        for edge, data in self._railway.graph.all_edges_with_data():
            edge_action = EdgeAction.NORMAL
            is_locked = self._railway.signalling.is_edge_locked(edge)
            is_platform = self._railway.stations.is_edge_platform(edge)
            is_in_preview = edge in self._state.preview.path
            is_occupied = self._railway.trains.is_edge_occupied(edge)

            if is_platform:
                edge_action = EdgeAction.PLATFORM
            elif is_occupied:
                continue #draw later
            elif is_in_preview:
                edge_action = EdgeAction.LOCKED_PREVIEW
            elif is_platform and is_locked:
                edge_action = EdgeAction.LOCKED_PLATFORM
            elif is_locked:
                edge_action = EdgeAction.LOCKED
            elif self._railway.stations.is_edge_platform(edge):
                edge_action = EdgeAction.PLATFORM
            draw_track(self._surface, edge, self._camera, edge_action, data["length"])

        for node in self._railway.graph_service.junctions:
            color = GREEN if self._railway.signalling.is_node_locked(node) else WHITE
            draw_node(self._surface, node, self._camera, color=color)

        for signal in self._railway.signals.all():
            color = RED
            if signal.next_signal is not None:
                color = GREEN
            if signal == self._state.selected_signal:
                color = LIME
            elif signal == self._state.preview.signal:
                color = LIGHTBLUE
            draw_signal(self._surface, signal, self._camera, color)

        for station in self._railway.stations.all():
            draw_station(self._surface, station, self._camera)

        for train in self._railway.trains.all():
            edges = train.occupied_edges()
            draw_occupied_edge(self._surface, edges[0].a, edges[0].b, self._camera, color=YELLOW, edge_progress=train.edge_progress, is_last=True)
            for edge in edges[1:-1]:
                draw_occupied_edge(self._surface, edge.a, edge.b, self._camera, color=YELLOW, edge_progress=train.edge_progress)
            draw_occupied_edge(self._surface, edges[-1].a, edges[-1].b, self._camera, color=YELLOW, edge_progress=train.edge_progress, is_first=True)

        if self._state.preview.signal is None and world_pos is not None:
            draw_node(self._surface, world_pos, self._camera, color=WHITE)
            
            
    def set_preview(self, world_pos: Position | None):
        self._state.preview.clear() 
        if world_pos is None:
            return
        
        snapped = world_pos.snap_to_grid()
        if self._railway.graph.has_node_at(snapped) and self._railway.signals.has_signal_at(snapped):
            signal = self._railway.signals.get(snapped)
            self._state.preview.signal = signal
            if self._state.selected_signal is None:
                return
            path = self._railway.signalling.get_path_preview(self._state.selected_signal, signal)
            self._state.preview.path = path if path is not None else []