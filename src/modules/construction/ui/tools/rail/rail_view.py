import pygame
from core.models.geometry.edge import Edge
from modules.construction.models.construction_view import ConstructionView
from core.models.geometry import Position
from core.config.color import Color
from shared.ui.enums.edge_action import EdgeAction
from shared.ui.utils import draw_node
from shared.ui.services.color_from_speed import color_from_speed
from shared.ui.utils.tracks import draw_rail, draw_track
from .rail_target import find_rail_target, RailTargetType

class RailView(ConstructionView):
    def render(self, world_pos: Position | None):
        if world_pos is None:
            if self._state.construction_anchor is not None:
                draw_node(self._surface, self._state.construction_anchor.position, self._camera, color=color_from_speed(self._state.track_speed))
            return

        target = find_rail_target(self._railway, world_pos, self._state.construction_anchor)

        color = color_from_speed(self._state.track_speed)

        if target.kind in (RailTargetType.NODE, RailTargetType.ANCHOR_SAME):
            draw_node(self._surface, target.snapped, self._camera, color=color)
            return
        
        if target.kind == RailTargetType.BLOCKED:
            draw_node(self._surface, target.snapped, self._camera, color=Color.RED)
            
            if self._state.construction_anchor is not None:
                draw_node(self._surface, self._state.construction_anchor.position, self._camera, color=color)
            return

        if target.kind == RailTargetType.NO_PATH:
            draw_node(self._surface, target.snapped, self._camera, color=Color.RED)
            if self._state.construction_anchor is not None:
                draw_node(self._surface, self._state.construction_anchor.position, self._camera, color=Color.RED)
            return

        # path preview
        screen_points = [Position(*pt) for pt in target.found_path]
        for line in zip(screen_points[:-1], screen_points[1:]):
            draw_track(self._surface, Edge(*line), camera=self._camera, edge_action=EdgeAction.SPEED, length=self._state.track_length, speed=self._state.track_speed)
        draw_node(self._surface, target.snapped, self._camera, color=color)
        draw_node(self._surface, self._state.construction_anchor.position, self._camera, color=color)
