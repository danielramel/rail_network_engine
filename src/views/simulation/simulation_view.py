from config.colors import GREEN, RED, WHITE, LIGHTBLUE
from graphics.camera import Camera
from models.construction_state import EdgeType
from models.geometry.position import Position
from models.railway_system import RailwaySystem
from models.simulation_state import SimulationState
from ui.models.base import UIComponent
from ui.utils import draw_train, draw_edge, draw_node, draw_signal, draw_station
import pygame

class SimulationView(UIComponent):
    def __init__(self, railway: RailwaySystem, camera: Camera, screen: pygame.Surface, simulation_state: SimulationState):
        self._surface = screen
        self._railway = railway
        self._camera = camera
        self._simulation_state = simulation_state
        
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
            draw_signal(self._surface, signal, self._camera, color=GREEN if signal.is_green else RED)

        for station in self._railway.stations.all():
            draw_station(self._surface, station, self._camera)

        for train in self._railway.trains.all():
            draw_train(self._surface, train, self._camera)
            
        if world_pos is None:
            return
        
        
        if self._simulation_state.selected_signal is not None:
            draw_signal(self._surface, self._simulation_state.selected_signal, self._camera, color=LIGHTBLUE)
            
        snapped = world_pos.snap_to_grid()
        if snapped is not None and self._railway.graph.has_node_at(snapped) and self._railway.signals.has_signal_at(snapped):
            draw_signal(self._surface, self._railway.signals.get(snapped), self._camera, color=LIGHTBLUE)
        else:
            draw_node(self._surface, world_pos, self._camera, color=WHITE)