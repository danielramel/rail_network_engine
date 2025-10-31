from controllers.construction.base_construction_controller import BaseConstructionController
from config.settings import PLATFORM_LENGTH
from ui.popups import alert
from services.construction.platform_target import find_platform_target
from graphics.camera import Camera
from models.railway_system import RailwaySystem
from models.construction_state import ConstructionState, EdgeType
import pygame
from views.construction.platform import PlatformView, PlatformTargetType

class PlatformController(BaseConstructionController):
    def __init__(self, railway: RailwaySystem, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        view = PlatformView(railway, state, camera, screen)
        super().__init__(view, railway, state, camera)


    def handle_event(self, event: pygame.event.Event) -> None:
        if event.button == 3:
            if self._construction_state.platform_waiting_for_station:
                self._construction_state.platform_waiting_for_station = False
            else:
                self._construction_state.switch_mode(None)
            return
                
        world_pos = self._camera.screen_to_world(event.screen_pos)
        # if user is currently selecting a station for the platform
        if self._construction_state.platform_waiting_for_station:
            for station in self._railway.stations.all():
                if world_pos.is_within_station_rect(station.position):
                    self._railway.platforms.add(station, list(self._construction_state.preview_edges))
                    break
            self._construction_state.platform_waiting_for_station = False
            return

        if len(self._railway.stations.all()) == 0:
            alert('Please build a station first.')
            self._construction_state.switch_mode(None)
            return

        target = find_platform_target(self._railway, world_pos, self._camera.scale)

        if target.kind in (PlatformTargetType.NONE, PlatformTargetType.EXISTING_PLATFORM):
            return

        if not target.is_valid:
            alert(f'Platform too short!')
            return

        # prepare to select station
        self._construction_state.platform_waiting_for_station = True
        self._construction_state.preview_edges_type = EdgeType.PLATFORM_SELECTED
