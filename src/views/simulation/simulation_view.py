from models.construction import EdgeType
from models.geometry.position import Position
from ui.components.base import BaseUIComponent
from ui.utils import draw_grid, draw_edge, draw_node, draw_signal, draw_station, draw_dotted_line

class SimulationView(BaseUIComponent):
    def __init__(self, map, camera, screen):
        self._surface = screen
        self._map = map
        self._camera = camera
        
    def render(self, screen_pos: Position | None) -> None:
        draw_grid(self._surface, self._camera)
    
        for edge in self._map.edges:
            if self._map.is_edge_platform(edge):
                draw_edge(self._surface, edge, self._camera, edge_type=EdgeType.PLATFORM)
            else:
                draw_edge(self._surface, edge, self._camera)

        for node in self._map.junctions:
            draw_node(self._surface, node, self._camera)

        for signal in self._map.signals:
            draw_signal(self._surface, signal, self._camera)

        for station in self._map.stations:
            draw_station(self._surface, station, self._camera)
            # for middle_point in self._map.get_platforms_middle_points(station):
            #     draw_dotted_line(self._surface, middle_point, station.position, self._camera, color=PURPLE)