from infrastructure.station_repository import StationRepository
from config.settings import PLATFORM_LENGTH
from domain.rail_map import GraphQueryService
from models.geometry import Position
from models.station import Station
from networkx import Graph


class StationPlatformService:
    def __init__(self, graph: Graph, query_service: GraphQueryService):
        self._repo = StationRepository()
        self._graph = graph
        self._query_service = query_service

    def add_station(self, pos: Position, name: str) -> Station:
        return self._repo.add(pos, name)
    
    def remove_station(self, pos: Position) -> None:
        self._repo.remove(pos)
        
    def move_station(self, old_pos: Position, new_pos: Position) -> None:
        self._repo.move(old_pos, new_pos)
    
    def get_station(self, pos: Position) -> Station:
        return self._repo.get(pos)
    
    def all_stations(self) -> dict[Position, Station]:
        return self._repo.all()


    def add(self, station: Station, edges: tuple[Position, Position]) -> None:
        for edge in edges:
            self._graph.edges[edge]['station'] = station
            
        station.platforms.add(edges)

    def remove(self, edge: tuple[Position, Position]) -> None:
        station = self._graph.edges[edge]['station']
        _, edges = self.get_platform(edge)
        for edge in edges:
            del self._graph.edges[edge]['station']
            
        station.platforms.remove(edges)

    def all(self) -> dict[tuple[Position, Position], Position]:
        return {edge: data['station'] for edge, data in self._graph.edges.items() if 'station' in data}
    
    def is_platform_at(self, pos: Position) -> bool:
        return all('station' in self._graph.edges[edge] for edge in self._graph.edges(pos))
    
    def is_edge_platform(self, edge: tuple[Position, Position]) -> bool:
        return 'station' in self._graph.edges[edge]
    
    def calculate_platform_preview(self, edge: tuple[Position, Position]) -> Position | None:
        # add 2 to max_nr to account for the edges that will be cut off at the ends
        _, edges = self.query_service.get_segment(edge, only_straight=True, max_nr=PLATFORM_LENGTH+2)
        sorted_edges = sorted(edges)[1:-1]  # remove the first and last edge to create a margin
        return sorted_edges
    
    def get_platform(self, edge: tuple[Position, Position]) -> set[tuple[Position, Position]]:
        _, edges = self.query_service.get_segment(edge, only_platforms=True)
        return edges
    
    def middle_points_with_corresponding_station_positions(self) -> dict[tuple[Position, Position], Position]:
        middle_points = dict()
        for edge in self.all():
            platform = self.get_platform(edge)
            middle_point = self.get_middle_of_platform(platform)
            station_pos = self._graph.edges[edge]['station'].position
            middle_points[middle_point] = station_pos
        return middle_points.items()
    
    def get_middle_of_platform(self, edges: tuple[tuple[Position, Position]]) -> Position | None:
        sorted_edges = sorted(edges)
        mid_edge = sorted_edges[len(sorted_edges) // 2]
        return mid_edge[0].midpoint(mid_edge[1])