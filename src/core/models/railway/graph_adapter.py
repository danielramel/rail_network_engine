from core.models.geometry import Position, Edge
import networkx as nx

from core.models.geometry.pose import Pose

class GraphAdapter:
    def __init__(self):
        self._graph = nx.Graph()
        
    @property
    def nodes(self) -> set[Position]:
        return self._graph.nodes
    
    @property
    def edges(self) -> frozenset[Edge]:
        return frozenset((Edge(*edge) for edge in self._graph.edges))
    
    def add_node(self, pos: Position) -> None:
        self._graph.add_node(pos)
        
    def has_node_at(self, pos: Position) -> bool:
        return pos in self._graph.nodes
    
    def remove_node(self, pos: Position) -> None:
        self._graph.remove_node(pos)
    
    def has_node_attr(self, pos: Position, key:str) -> bool:
        return key in self._graph.nodes[pos]
    
    def get_node_attr(self, pos: Position, key:str) -> dict:
        return self._graph.nodes[pos].get(key, None)
    
    def set_node_attr(self, pos: Position, key: str, value) -> None:
        self._graph.nodes[pos][key] = value
        
    def remove_node_attr(self, pos: Position, key: str) -> None:
        if pos in self._graph.nodes and key in self._graph.nodes[pos]:
            del self._graph.nodes[pos][key]
    
    def all_nodes_with_attr(self, key: str) -> dict[Position, dict]:
        return {n: data[key] for n, data in self._graph.nodes(data=True) if key in data}
    
    def degree_at(self, pos: Position) -> int:
        return self._graph.degree[pos]
    
    def has_edge(self, edge: Edge) -> bool:
        return self._graph.has_edge(*edge)
    
    def set_edge_attr(self, edge: Edge, key: str, value) -> None:
        self._graph.edges[edge][key] = value
        
    def has_edge_attr(self, edge: Edge, key: str) -> bool:
        return key in self._graph.edges[edge]
        
    def get_edge_attr(self, edge: Edge, key: str) -> dict:
        return self._graph.edges[edge].get(key, None)
    
    def remove_edge_attr(self, edge: Edge, key: str) -> None:
        del self._graph.edges[edge][key]
        
    def get_edge_length(self, edge: Edge) -> int:
        return self._graph.edges[edge]['length']
    
    def get_edge_speed(self, edge: Edge) -> int:
        return self._graph.edges[edge]['speed']

    def all_edges_with_data(self) -> list[tuple[Edge, dict]]:
        return [(Edge(a, b), data) for a, b, data in self._graph.edges(data=True)]

    def neighbors(self, pos: Position) -> tuple[Position]:
        return tuple(self._graph.neighbors(pos))
    
    def get_dead_end_poses(self) -> list[Pose]:
        nodes = [node for node, degree in self._graph.degree() if degree == 1]
        return [Pose(node, next(iter(self._graph.neighbors(node))).direction_to(node)) for node in nodes]


    def add_edge(self, a: Position, b: Position, speed: int, length: int) -> None:
        self._graph.add_edge(a, b, speed=speed, length=length)

    def remove_edge(self, edge: Edge) -> None:
        self._graph.remove_edge(edge.a, edge.b)
        
    def get_edges(self, pos: Position) -> list[Edge]:
        return self._graph.edges(pos)
        
        
    def to_dict(self) -> dict:
        graph_data = nx.node_link_data(self._graph, edges="edges")
        
        # convert Position objects in node attributes to dicts
        for node in graph_data['nodes']:
            node['id'] = node['id'].to_dict()
            for key in list(node.keys()):
                if key != "id":
                    del node[key]
            
        for edge in graph_data['edges']:
            edge["source"] = edge["source"].to_dict()
            edge["target"] = edge["target"].to_dict()
            for key in list(edge.keys()):
                if key not in ("source", "target", "speed", "length"):
                    del edge[key]
        
        return graph_data
    
    @classmethod
    def from_dict(cls, graph_data: dict) -> None:
        instance = cls()
        
        for node in graph_data['nodes']:
            node['id'] = Position.from_dict(node['id'])
            
        for edge in graph_data['edges']:
            edge['source'] = Position.from_dict(edge['source'])
            edge['target'] = Position.from_dict(edge['target'])

        instance._graph = nx.node_link_graph(graph_data, edges="edges")
        
        return instance