import pygame
from core.config.color import Color
from core.config.settings import Config
from modules.simulation.ui.simulation_target import SimulationTargetType, find_simulation_target
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.utils.grid import draw_grid
from shared.ui.utils.tracks import draw_track
from shared.ui.utils.nodes import draw_junction_node, draw_node
from shared.ui.utils.signal import draw_signal
from shared.ui.utils.station import draw_station
from shared.ui.utils.lines import draw_dotted_line
from shared.ui.utils.train import draw_train
from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from modules.simulation.models.simulation_state import SimulationState
from shared.ui.enums.edge_action import EdgeAction
from core.models.geometry.position import Position


class SimulationView(ClickableUIComponent, FullScreenUIComponent):
    def __init__(self, railway: RailwaySystem, simulation_state: SimulationState, graphics: GraphicsContext):
        self._railway = railway
        self._state = simulation_state
        self._screen = graphics.screen
        self._camera = graphics.camera
        
    def render(self, world_pos: Position | None) -> None:
        self._state.preview.clear()
            
        target = find_simulation_target(self._railway, world_pos)
        
        preview_path = []
        if target.kind is SimulationTargetType.SIGNAL and self._state.selected_signal is not None:
            path = self._railway.signalling.get_path_preview(self._state.selected_signal, target.signal)
            if path is not None:
                preview_path = path
            
            
        draw_grid(self._screen, self._camera)
        for edge, data in self._railway.graph.all_edges_with_data():
            edge_action = EdgeAction.NO_SPEED
            is_locked = self._railway.signalling.is_edge_locked(edge)
            is_platform = self._railway.stations.is_edge_platform(edge)
            is_in_preview = edge in preview_path

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
            draw_junction_node(self._screen, node, self._camera, Color.WHITE)
            
        for node in self._railway.graph.all_nodes_with_attr("blocked"):
            draw_node(self._screen, node, self._camera, color=Color.RED)

        shift_pressed = bool(pygame.key.get_mods() & pygame.KMOD_SHIFT)
        for signal in self._railway.signals.all():            
            automatic = signal.pose in self._railway.signalling.auto_signals
            if signal is self._state.selected_signal:
                automatic = automatic or shift_pressed
                color = Color.LIME
            elif target.signal == signal:
                automatic = automatic or (shift_pressed and self._state.selected_signal is None)
                color = Color.LIGHTBLUE
            elif signal.next_signal is not None:
                color = Color.GREEN
            elif automatic:
                color = Color.ORANGE
            else:
                color = Color.RED
                
            draw_signal(self._screen, signal, self._camera, color, automatic=automatic)
        
        for station in self._railway.stations.all():
            draw_station(self._screen, station, self._camera)

        for train in self._railway.trains.all():
            if train.schedule is not None:
                color = Color.get(train.schedule.color)
            elif train.live:
                color = Config.TRAIN_LIVE_COLOR
            else:
                color = Config.TRAIN_SHUTDOWN_COLOR
                
            draw_train(self._screen, train, self._camera, color, lighten_flag=target.train_id == train.id, locomotive_different=True)

        if target.kind is SimulationTargetType.NODE and self._state.selected_signal is not None:
            color = Color.GREEN if self._railway.graph.get_node_attr(target.node, "blocked") else Color.RED
            draw_node(self._screen, target.node, self._camera, color=color)
            
        elif target.kind is SimulationTargetType.NONE or target.kind is SimulationTargetType.NODE:
            draw_node(self._screen, target.node, self._camera, color=Color.LIME)
            
            if self._state.selected_signal is not None and len(self._state.preview.path) == 0:
                draw_dotted_line(self._screen, self._state.selected_signal.node, target.node, self._camera, color=Color.LIME)