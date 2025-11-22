from core.models.geometry.edge import Edge
import networkx as nx

from core.models.rail import Rail
from core.models.geometry.pose import Pose
from core.models.geometry.node import Node

class GraphAdapter:
    def __init__(self):
        self._graph = nx.Graph()
        
    @property
    def nodes(self) -> set[Node]:
        return self._graph.nodes
    
    @property
    def edges(self) -> frozenset[Edge]:
        return frozenset((Edge(*edge) for edge in self._graph.edges))
    
    def add_node(self, node: Node) -> None:
        self._graph.add_node(node)
        
    def has_node_at(self, node: Node) -> bool:
        return node in self._graph.nodes
    
    def remove_node(self, node: Node) -> None:
        self._graph.remove_node(node)
    
    def has_node_attr(self, node: Node, key:str) -> bool:
        return key in self._graph.nodes[node]
    
    def get_node_attr(self, node: Node, key:str) -> dict:
        return self._graph.nodes[node].get(key, None)
    
    def set_node_attr(self, node: Node, key: str, value) -> None:
        self._graph.nodes[node][key] = value
        
    def remove_node_attr(self, node: Node, key: str) -> None:
        if node in self._graph.nodes and key in self._graph.nodes[node]:
            del self._graph.nodes[node][key]
    
    def all_nodes_with_attr(self, key: str) -> dict[Node, dict]:
        return {n: data[key] for n, data in self._graph.nodes(data=True) if key in data}
    
    def degree_at(self, node: Node) -> int:
        return self._graph.degree[node]
    
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
    
    def get_rail(self, edge: Edge) -> Rail:
        return Rail(edge=edge, speed=self.get_edge_speed(edge), length=self.get_edge_length(edge))

    def all_edges_with_data(self) -> list[tuple[Edge, dict]]:
        return [(Edge(a, b), data) for a, b, data in self._graph.edges(data=True)]

    def neighbors(self, node: Node) -> tuple[Node]:
        return tuple(self._graph.neighbors(node))
    
    def get_dead_end_poses(self) -> list[Pose]:
        nodes = [node for node, degree in self._graph.degree() if degree == 1]
        return [Pose(node, next(iter(self._graph.neighbors(node))).direction_to(node)) for node in nodes]


    def add_edge(self, a: Node, b: Node, speed: int, length: int) -> None:
        self._graph.add_edge(a, b, speed=speed, length=length)

    def remove_edge(self, edge: Edge) -> None:
        self._graph.remove_edge(edge.a, edge.b)
        
    def get_edges(self, node: Node) -> list[Edge]:
        return self._graph.edges(node)
        
        
    def to_dict(self) -> dict:
        graph_data = nx.node_link_data(self._graph, edges="edges")
        
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
            node['id'] = Node.from_dict(node['id'])
            
        for edge in graph_data['edges']:
            edge['source'] = Node.from_dict(edge['source'])
            edge['target'] = Node.from_dict(edge['target'])

        instance._graph = nx.node_link_graph(graph_data, edges="edges")
        
        return instance