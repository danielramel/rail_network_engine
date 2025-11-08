from core.config.colors import BLUE, GREEN, GREY, LIME, RED, WHITE, LIGHTBLUE, YELLOW
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.utils import draw_grid, draw_track, draw_node, draw_signal, draw_station, draw_train
from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from shared.ui.enums.edge_action import EdgeAction
from core.models.geometry.position import Position
from modules.setup.models.setup_state import SetupState
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent


class SetupView(ClickableUIComponent, FullScreenUIComponent):
    def __init__(self, railway: RailwaySystem, setup_state: SetupState, graphics: GraphicsContext):
        self._railway = railway
        self._surface = graphics.screen
        self._camera = graphics.camera
        self._state = setup_state

    def render(self, world_pos: Position | None) -> None:
        self.set_preview(world_pos)
        
        draw_grid(self._surface, self._camera)
        for edge, data in self._railway.graph.all_edges_with_data():
            speed = data.get('speed')
            length = data.get('length')
            
            if self._railway.stations.is_edge_platform(edge):
                edge_action = EdgeAction.PLATFORM
            elif self._railway.trains.get_train_on_edge(edge):
                continue #draw later
            else:
                edge_action = EdgeAction.SPEED

            draw_track(self._surface, edge, self._camera, edge_action, length=length, speed=speed)

        for node in self._railway.graph_service.junctions:
            draw_node(self._surface, node, self._camera, color=WHITE)

        for signal in self._railway.signals.all():
            draw_signal(self._surface, signal, self._camera, RED)

        for station in self._railway.stations.all():
            draw_station(self._surface, station, self._camera)

        for train in self._railway.trains.all():
            edges = train.occupied_edges()
            if self._state.preview.edge in edges:
                color = LIGHTBLUE
            else:
                color = YELLOW
            draw_train(self._surface, edges, self._camera, edge_progress=train.edge_progress)

        if self._state.preview.edge is not None:
            platform = self._railway.stations.get_platform_from_edge(self._state.preview.edge)
            edges = [edge.ordered(self._state.preview.reversed) for edge in sorted(platform, reverse=self._state.preview.reversed)]
            draw_train(self._surface, edges, self._camera, edge_progress=1.0)
        elif world_pos is not None:
            draw_node(self._surface, world_pos, self._camera, color=WHITE)
            
    def set_preview(self, world_pos: Position | None) -> None:
        if world_pos is None:
            return
        self._state.preview.clear()
        closest_edge = world_pos.closest_edge(self._railway.graph.edges, self._camera.scale)
        if closest_edge and self._railway.stations.is_edge_platform(closest_edge):
            self._state.preview.edge = closest_edge
            train = self._railway.trains.get_train_on_edge(closest_edge)
            if train is not None:
                locomotive_edge = train.occupied_edges()[0]
                self._state.preview.reversed = locomotive_edge.a < locomotive_edge.b