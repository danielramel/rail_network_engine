from controllers.construction.base_construction_controller import BaseConstructionController
from models.event import CLICK_TYPE, Event
from config.settings import PLATFORM_LENGTH
from ui.popups import alert
from services.construction.platform_target import find_platform_target
from graphics.camera import Camera
from models.simulation import Simulation
from models.construction import ConstructionState, EdgeType
import pygame
from views.construction.platform import PlatformView, PlatformTargetType

class PlatformController(BaseConstructionController):
    def __init__(self, simulation: Simulation, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        view = PlatformView(simulation, state, camera, screen)
        super().__init__(view, simulation, state, camera)
        
        
    def handle_event(self, event: Event):
        if event.click_type == CLICK_TYPE.RIGHT_CLICK:
            if self._construction_state.platform_waiting_for_station:
                self._construction_state.platform_waiting_for_station = False
            else:
                self._construction_state.switch_mode(None)
            return
                
        world_pos = self._camera.screen_to_world(event.screen_pos)
        # if user is currently selecting a station for the platform
        if self._construction_state.platform_waiting_for_station:
            for station in self._simulation.stations.all():
                if world_pos.is_within_station_rect(station.position):
                    self._simulation.platforms.add(station, list(self._construction_state.preview_edges))
                    break
            self._construction_state.platform_waiting_for_station = False
            return

        if len(self._simulation.stations.all()) == 0:
            alert('Please build a station first.')
            self._construction_state.switch_mode(None)
            return

        target = find_platform_target(self._simulation, world_pos, self._camera.scale)

        if target.kind in (PlatformTargetType.NONE, PlatformTargetType.EXISTING_PLATFORM):
            return

        if not target.is_valid:
            alert(f'Platform too short!')
            return

        # prepare to select station
        self._construction_state.platform_waiting_for_station = True
        self._construction_state.preview_edges_type = EdgeType.PLATFORM_SELECTED
