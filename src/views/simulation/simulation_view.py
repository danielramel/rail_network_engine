from config.colors import BLUE, GREEN, LIME, RED, WHITE, LIGHTBLUE
from models.construction_state import EdgeAction
from models.geometry.position import Position
from models.railway_system import RailwaySystem
from models.simulation_state import SimulationState
from ui.models.ui_component import UIComponent
from ui.utils import draw_train, draw_edge, draw_node, draw_signal, draw_station
from graphics.graphics_context import GraphicsContext

class SimulationView(UIComponent):
    def __init__(self, railway: RailwaySystem, simulation_state: SimulationState, graphics: GraphicsContext):
        self._railway = railway
        self._state = simulation_state
        self._surface = graphics.screen
        self._camera = graphics.camera
        
    def render(self, world_pos: Position | None) -> None:
        # draw_grid(self._surface, self._camera)
        self.set_preview(world_pos)
        
        for edge in self._railway.graph.edges:
            edge_action = EdgeAction.NORMAL
            if edge in self._state.preview.path:
                edge_action = EdgeAction.LOCKED_PREVIEW
            elif self._railway.stations.is_edge_platform(edge) and self._railway.signalling.is_edge_locked(edge):
                edge_action = EdgeAction.LOCKED_PLATFORM
            elif self._railway.signalling.is_edge_locked(edge):
                edge_action = EdgeAction.LOCKED
            elif self._railway.stations.is_edge_platform(edge):
                edge_action = EdgeAction.PLATFORM
            draw_edge(self._surface, edge, self._camera, edge_action)

        for node in self._railway.graph_service.junctions:
            draw_node(self._surface, node, self._camera)

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
            draw_train(self._surface, train, self._camera)

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