import networkx as nx
from models.geometry import Position, Pose, Edge
from models.schedule import Schedule
from services.rail.graph_query_service import GraphService
from services.rail.signal_service import SignalService
from services.rail.path_finder import Pathfinder
from services.rail.platform_service import PlatformService
from models.station import StationRepository
from services.schedule_service import ScheduleService

class Simulation:
    def __init__(self):
        self._graph = nx.Graph()
        self._graph_service = GraphService(self._graph)
        self._signal_service = SignalService(self._graph, self)
        self._platform_service = PlatformService(self._graph, self)
        self._pathfinder = Pathfinder(self)
        self._station_repository = StationRepository()
        self._schedule_service = ScheduleService()
    
    @property
    def graph(self) -> GraphService:
        return self._graph_service
    
    @property
    def signals(self) -> SignalService:
        return self._signal_service
    
    @property
    def schedules(self) -> ScheduleService:
        return self._schedule_service
            
            
    # --- pathfinding ---
    def is_blocked(self, pos: Position) -> bool:
        return self._pathfinder.is_blocked(pos)

    def find_path(self, start: Pose, end: Position) -> list[Position] | None:
        return self._pathfinder.find_grid_path(start, end)

    # --- stations ---
    @property
    def stations(self) -> StationRepository:
        return self._station_repository

    def remove_station_at(self, pos: Position):
        station = self._station_repository.remove(pos)
        for platforms in station.platforms:
            self._platform_service.remove(platforms)
    
    # --- platforms ---
    @property
    def platforms(self) -> PlatformService:
        return self._platform_service

    def remove_platform_at(self, edge: Edge):
        platform_edges = self.platforms.get_platform_from_edge(edge)
        station = self._graph.edges[edge]['station']
        self._platform_service.remove(platform_edges)
        self._station_repository.remove_platform_from_station(station, platform_edges)
    
    # -- serialization ---
    def to_dict(self) -> dict:
        graph_data = nx.node_link_data(self._graph)
        
        # convert Position objects in node attributes to dicts
        for node in graph_data['nodes']:
            node['id'] = node['id'].to_dict()
            
        for link in graph_data['links']:
            for key in ('source', 'target'):
                link[key] = link[key].to_dict()
            if 'station' in link:
                link['station'] = link['station'].to_dict_simple()
            
        station_data = self._station_repository.to_dict()

        return {
            'graph': graph_data,
            'stations': station_data,
            'schedules': [schedule.to_dict() for schedule in self._schedule_service]
        }
        

    def from_dict(self, data: dict) -> None:
        graph_data = data['graph']
        self._station_repository = StationRepository.from_dict(data['stations'])
        self._schedule_service = [Schedule.from_dict(schedule_data, self) for schedule_data in data['schedules']]

        # convert dicts in node attributes back to Position objects
        for node in graph_data['nodes']:
            node['id'] = Position.from_dict(node['id'])
            if 'signal' in node:
                node['signal'] = tuple(node['signal'])
            
        for link in graph_data['links']:
            for key in ('source', 'target'):
                link[key] = Position.from_dict(link[key])
            if 'station' in link:
                pos = Position.from_dict(link['station']['position'])
                link['station'] = self.stations.get(pos)

        temp_graph = nx.node_link_graph(graph_data)
        
        self._graph.clear()
        self._graph.add_nodes_from(temp_graph.nodes(data=True))
        self._graph.add_edges_from(temp_graph.edges(data=True))
        
        
    