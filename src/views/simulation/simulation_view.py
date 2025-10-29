from config.colors import BLUE, GREEN, RED
from graphics.camera import Camera
from models.construction import EdgeType
from models.geometry.position import Position
from models.railway_system import RailwaySystem
from ui.models.base import UIComponent
from ui.utils import draw_train, draw_edge, draw_node, draw_signal, draw_station
import pygame

class SimulationView(UIComponent):
    def __init__(self, railway: RailwaySystem, camera: Camera, screen: pygame.Surface):
        self._surface = screen
        self._railway = railway
        self._camera = camera
        
    def render(self, world_pos: Position | None) -> None:
        # draw_grid(self._surface, self._camera)
    
        for edge in self._railway.graph.edges:
            if self._railway.platforms.is_edge_platform(edge):
                draw_edge(self._surface, edge, self._camera, edge_type=EdgeType.PLATFORM)
            else:
                draw_edge(self._surface, edge, self._camera)

        for node in self._railway.graph.junctions:
            draw_node(self._surface, node, self._camera)

        for signal in self._railway.signals.all():
            draw_signal(self._surface, signal, self._camera, color=GREEN if signal.allowed else RED)

        for station in self._railway.stations.all():
            draw_station(self._surface, station, self._camera)

        for train in self._railway.trains.all():
            draw_train(self._surface, train, self._camera)
            
        if world_pos is None:
            return
        
        draw_node(self._surface, world_pos.snap_to_grid(), self._camera, color=GREEN)
