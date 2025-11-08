from core.config.colors import BLUE, GREEN, LIME, RED, WHITE, LIGHTBLUE, YELLOW
from shared.ui.models.clickable_component import ClickableComponent
from shared.ui.utils import draw_grid, draw_track, draw_node, draw_signal, draw_station, draw_occupied_edge
from core.graphics.graphics_context import GraphicsContext
from core.models.railway.railway_system import RailwaySystem
from core.models.edge_action import EdgeAction
from core.models.geometry.position import Position


class SetupView(ClickableComponent):
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
                edge_action = EdgeAction.PLATFORM
            elif self._railway.trains.is_edge_occupied(edge):
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
            for edge in edges:
                draw_occupied_edge(self._surface, edge.a, edge.b, self._camera, color=YELLOW, edge_progress=train.edge_progress)

        if world_pos is None:
            return
        
        closest_edge = world_pos.closest_edge(self._railway.graph.edges, self._camera.scale)
        if closest_edge and self._railway.stations.is_edge_platform(closest_edge):
            platform = self._railway.stations.get_platform_from_edge(closest_edge)
            for edge in platform:
                a, b = edge.ordered()
                draw_occupied_edge(self._surface, a, b, self._camera, color=LIGHTBLUE, edge_progress=1.0)
        else:
            draw_node(self._surface, world_pos, self._camera, color=WHITE)