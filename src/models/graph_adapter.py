from models.geometry import Position, Edge
import networkx as nx

class GraphAdapter:
    def __init__(self, graph: nx.Graph):
        self._graph = graph
        
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

    def all_edges_with_attr(self, key: str) -> list[tuple[Edge, object]]:
        return [(Edge(a, b), data[key]) for a, b, data in self._graph.edges(data=True) if key in data]

    def neighbors(self, pos: Position) -> tuple[Position]:
        return tuple(self._graph.neighbors(pos))
    
        
    def add_edge(self, a: Position, b: Position, speed: int) -> None:
        self._graph.add_edge(a, b, speed=speed)

    def remove_edge(self, edge: Edge) -> None:
        self._graph.remove_edge(edge.a, edge.b)
        
    def get_edges(self, pos: Position) -> list[Edge]:
        return self._graph.edges(pos)
        
        
    def to_dict(self) -> dict:
        graph_data = nx.node_link_data(self._graph)
        
        # convert Position objects in node attributes to dicts
        for node in graph_data['nodes']:
            node['id'] = node['id'].to_dict()
            if 'signal' in node:
                node['signal'] = node['signal'].to_dict()
            
        for link in graph_data['links']:
            link["source"] = link["source"].to_dict()
            link["target"] = link["target"].to_dict()
            if 'station' in link:
                link['station'] = link['station'].id
        
        return graph_data
    
    

    def from_dict(self, graph_data: dict) -> None:
        from models.signal import Signal
        
        for node in graph_data['nodes']:
            node['id'] = Position.from_dict(node['id'])
            if 'signal' in node:
                node['signal'] = Signal.from_dict(node['signal'])
            
        for link in graph_data['links']:
            for key in ('source', 'target'):
                link[key] = Position.from_dict(link[key])

        temp_graph = nx.node_link_graph(graph_data)
        
        self._graph.clear()
        self._graph.add_nodes_from(temp_graph.nodes(data=True))
        self._graph.add_edges_from(temp_graph.edges(data=True))