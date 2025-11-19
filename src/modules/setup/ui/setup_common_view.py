from core.config.color import Color
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.utils import draw_grid, draw_track, draw_node, draw_signal, draw_station, draw_train, TRAINDRAWACTION
from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from shared.ui.enums.edge_action import EdgeAction
from core.models.geometry.position import Position
from modules.setup.models.setup_state import SetupAction, SetupState
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent


class SetupCommonView(ClickableUIComponent, FullScreenUIComponent):
    def __init__(self, railway: RailwaySystem, setup_state: SetupState, graphics: GraphicsContext):
        self._railway = railway
        self._surface = graphics.screen
        self._camera = graphics.camera
        self._state = setup_state

    def render(self, screen_pos: Position | None) -> None:        
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
            draw_node(self._surface, node, self._camera, color=Color.WHITE, junction=True)

        for signal in self._railway.signals.all():
            draw_signal(self._surface, signal, self._camera, Color.RED)

        for station in self._railway.stations.all():
            draw_station(self._surface, station, self._camera)

        for train in self._railway.trains.all():
            edges = train.get_occupied_edges()
            if self._state.preview.edge in edges and self._state.preview.action is SetupAction.REMOVE:
                continue
            draw_train(self._surface, train, self._camera, TRAINDRAWACTION.SHUTDOWN)

        if self._state.preview.edge is not None and self._state.preview.action is SetupAction.ADD:
            train = self._railway.trains.get_preview_train_on_platform_edge(self._state.preview.edge)
            draw_train(self._surface, train, self._camera, TRAINDRAWACTION.SHUTDOWN)