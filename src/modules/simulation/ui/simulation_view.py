from core.config.color import Color
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.utils import draw_track, draw_node, draw_signal, draw_station, draw_train, draw_dotted_line, draw_grid
from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from modules.simulation.models.simulation_state import SimulationState
from shared.ui.enums.edge_action import EdgeAction
from core.models.geometry.position import Position
from shared.ui.utils.train import TRAINDRAWACTION


class SimulationView(ClickableUIComponent, FullScreenUIComponent):
    def __init__(self, railway: RailwaySystem, simulation_state: SimulationState, graphics: GraphicsContext):
        self._railway = railway
        self._state = simulation_state
        self._screen = graphics.screen
        self._camera = graphics.camera
        
    def render(self, world_pos: Position | None) -> None:
        self.set_preview(world_pos)
        
        draw_grid(self._screen, self._camera)

        for edge, data in self._railway.graph.all_edges_with_data():
            edge_action = EdgeAction.NORMAL
            is_locked = self._railway.signalling.is_edge_locked(edge)
            is_platform = self._railway.stations.is_edge_platform(edge)
            is_in_preview = edge in self._state.preview.path

            if is_platform and is_locked:
                edge_action = EdgeAction.LOCKED_PLATFORM
            elif is_platform:
                edge_action = EdgeAction.PLATFORM
            elif is_in_preview:
                edge_action = EdgeAction.LOCKED_PREVIEW
            elif is_locked:
                edge_action = EdgeAction.LOCKED
            elif self._railway.stations.is_edge_platform(edge):
                edge_action = EdgeAction.PLATFORM
            draw_track(self._screen, edge, self._camera, edge_action, data["length"])

        for node in self._railway.graph_service.junctions:
            color = Color.GREEN if self._railway.signalling.is_node_locked(node) else Color.WHITE
            draw_node(self._screen, node, self._camera, color=color, junction=True)

        for signal in self._railway.signals.all():
            color = Color.RED
            if signal.next_signal is not None:
                color = Color.GREEN
            if signal == self._state.selected_signal:
                color = Color.LIME
            elif signal == self._state.preview.signal:
                color = Color.LIGHTBLUE
            draw_signal(self._screen, signal, self._camera, color)
        

        for station in self._railway.stations.all():
            draw_station(self._screen, station, self._camera)

        for train in self._railway.trains.all():
            if self._state.preview.train_id == train.id and train.id not in self._state.selected_trains:
                action = TRAINDRAWACTION.PREVIEWED
            elif train.id in self._state.selected_trains:
                action = TRAINDRAWACTION.SELECTED
            elif train.timetable is not None:
                action = TRAINDRAWACTION.SCHEDULED
            elif train.is_live:
                action = TRAINDRAWACTION.LIVE
            else:
                action = TRAINDRAWACTION.SHUTDOWN
            
            draw_train(self._screen, train, self._camera, action)

        
        if self._state.preview.signal is None and world_pos is not None:
            draw_node(self._screen, world_pos, self._camera, color=Color.LIME)
            
            if self._state.selected_signal is not None and len(self._state.preview.path) == 0:
                draw_dotted_line(self._screen, self._state.selected_signal.node, world_pos, self._camera, color=Color.LIME)
            
            
    def set_preview(self, world_pos: Position | None):
        self._state.preview.clear()
        if world_pos is None:
            return
        
        snapped = world_pos.snap_to_grid()
        if self._railway.signals.has_signal_at(snapped):
            signal = self._railway.signals.get(snapped)
            self._state.preview.signal = signal
            if self._state.selected_signal is None:
                return
            path = self._railway.signalling.get_path_preview(self._state.selected_signal, signal)
            self._state.preview.path = path if path is not None else []
            
        closest_edge = self._railway.graph_service.get_closest_edge(world_pos, self._camera.scale)
        train_id = closest_edge is not None and self._railway.trains.get_train_on_edge(closest_edge)
        if train_id:
            self._state.preview.train_id = train_id