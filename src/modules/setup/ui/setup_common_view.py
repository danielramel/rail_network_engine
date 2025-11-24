from core.config.color import Color
from core.config.settings import Config
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from shared.ui.utils.nodes import draw_junction_node
from shared.ui.utils.tracks import draw_track
from shared.ui.utils.signal import draw_signal
from shared.ui.utils.station import draw_station
from shared.ui.utils.train import draw_train
from shared.ui.utils.grid import draw_grid
from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from shared.ui.enums.edge_action import EdgeAction
from core.models.geometry.position import Position
from modules.setup.models.setup_state import SetupState
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent


class SetupCommonView(ClickableUIComponent, FullScreenUIComponent):
    def __init__(self, railway: RailwaySystem, setup_state: SetupState, graphics: GraphicsContext):
        self._railway = railway
        self._screen = graphics.screen
        self._camera = graphics.camera
        self._state = setup_state

    def render(self, screen_pos: Position | None) -> None:        
        draw_grid(self._screen, self._camera)
        
        for edge, data in self._railway.graph.all_edges_with_data():
            speed = data.get('speed')
            length = data.get('length')
            if self._railway.stations.is_edge_platform(edge):
                if edge in self._state.preview.invalid_platform_edges:
                    edge_action = EdgeAction.INVALID_PLATFORM
                else:
                    edge_action = EdgeAction.PLATFORM
            else:
                edge_action = EdgeAction.SPEED

            draw_track(self._screen, edge, self._camera, edge_action, length=length, speed=speed)

        for node in self._railway.graph_service.junctions:
            draw_junction_node(self._screen, node, self._camera)

        for signal in self._railway.signals.all():
            draw_signal(self._screen, signal, self._camera, Color.RED)

        for station in self._railway.stations.all():
            draw_station(self._screen, station, self._camera)

        for train in self._railway.trains.all():
            if self._state.preview.train_id_to_remove == train.id:
                draw_train(self._screen, train, self._camera, Color.RED)
                continue
            draw_train(self._screen, train, self._camera, Config.TRAIN_SHUTDOWN_COLOR)

        if self._state.preview.train_to_preview is not None:
            draw_train(self._screen, self._state.preview.train_to_preview, self._camera, Config.TRAIN_LIVE_COLOR)