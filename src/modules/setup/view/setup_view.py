from core.config.colors import BLUE, GREEN, LIME, RED, WHITE, LIGHTBLUE
from shared.ui.models.ui_component import UIComponent
from shared.ui.utils import draw_grid, draw_track, draw_node, draw_signal, draw_station
from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from modules.simulation.models.simulation_state import SimulationState
from core.models.edge_action import EdgeAction
from core.models.geometry.position import Position


class SetupView(UIComponent):
    def __init__(self, railway: RailwaySystem, graphics: GraphicsContext):
        self._railway = railway
        self._surface = graphics.screen
        self._camera = graphics.camera
        
    def render(self, world_pos: Position | None) -> None:
        draw_grid(self._surface, self._camera)
        for edge, data in self._railway.graph.all_edges_with_data():
            speed = data.get('speed')
            length = data.get('length')
            if self._railway.stations.is_edge_platform(edge):
                draw_track(self._surface, edge, self._camera, EdgeAction.PLATFORM, length=length)
            else:
                draw_track(self._surface, edge, self._camera, EdgeAction.SPEED, speed=speed, length=length)

        for node in self._railway.graph_service.junctions:
            draw_node(self._surface, node, self._camera, color=WHITE)

        for signal in self._railway.signals.all():
            draw_signal(self._surface, signal, self._camera, RED)

        for station in self._railway.stations.all():
            draw_station(self._surface, station, self._camera)

        # for train in self._railway.trains.all():
        #     draw_train(self._surface, train, self._camera)
        if world_pos is None:
            return
        
        draw_node(self._surface, world_pos, self._camera, color=WHITE)