from graphics.camera import Camera
from models.construction import EdgeType
from models.geometry.position import Position
from models.simulation import Simulation
from ui.models.base import UIComponent
from ui.utils import draw_grid, draw_edge, draw_node, draw_signal, draw_station, draw_dotted_line
import pygame

class SimulationView(UIComponent):
    def __init__(self, simulation: Simulation, camera: Camera, screen: pygame.Surface):
        self._surface = screen
        self._simulation = simulation
        self._camera = camera
        
    def render(self, screen_pos: Position | None) -> None:
        # draw_grid(self._surface, self._camera)
    
        for edge in self._simulation.graph.edges:
            if self._simulation.platforms.is_edge_platform(edge):
                draw_edge(self._surface, edge, self._camera, edge_type=EdgeType.PLATFORM)
            else:
                draw_edge(self._surface, edge, self._camera)

        for node in self._simulation.graph.junctions:
            draw_node(self._surface, node, self._camera)

        for signal in self._simulation.signals.all():
            draw_signal(self._surface, signal, self._camera)

        for station in self._simulation.stations.all():
            draw_station(self._surface, station, self._camera)
            # for middle_point in self._map.get_platforms_middle_points(station):
            #     draw_dotted_line(self._surface, middle_point, station.position, self._camera, color=PURPLE)