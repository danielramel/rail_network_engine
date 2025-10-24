import pygame
from controllers.construction.base_construction_controller import BaseConstructionController
from services.construction.rail_target import find_rail_target, RailTargetType
from models.geometry import Pose
from views.construction.rail import RailView
from graphics.camera import Camera
from models.simulation import Simulation
from models.construction import ConstructionState

class RailController(BaseConstructionController):
    def __init__(self, simulation: Simulation, state: ConstructionState, camera: Camera, screen: pygame.Surface):
        view = RailView(simulation, state, camera, screen)
        super().__init__(view, simulation, state, camera)
        
        
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.button == 3:
            if self._construction_state.construction_anchor is not None:
                self._construction_state.construction_anchor = None
            else:
                self._construction_state.switch_mode(None)
            return

        target = find_rail_target(self._simulation, self._camera.screen_to_world(event.screen_pos), self._construction_state.construction_anchor)

        if target.kind == RailTargetType.NODE:
            self._construction_state.construction_anchor = Pose(target.snapped, (0, 0))

        elif target.kind == RailTargetType.ANCHOR_SAME:
            self._construction_state.construction_anchor = None


        elif target.kind == RailTargetType.PATH:
            self._simulation.graph.add_segment(target.found_path, self._construction_state.track_speed)
            self._construction_state.construction_anchor = Pose(
                target.snapped,
                target.found_path[-2].direction_to(target.snapped)
            )
