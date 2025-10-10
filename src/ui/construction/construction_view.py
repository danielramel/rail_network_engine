from domain.rail_map import RailMap
from models.construction import ConstructionState
from graphics.camera import Camera
import pygame

class ConstructionView:
    def __init__(self, map: RailMap, state: ConstructionState, camera: Camera, surface: pygame.Surface):
        self._map = map
        self._construction_state = state
        self._camera = camera
        self._surface = surface