import pygame
from views.construction.base_construction_view import BaseConstructionView
from models.geometry import Position
from config.colors import RED
from ui.utils import draw_node, color_from_speed
from services.construction.rail_target import find_rail_target, RailTargetType

class RailView(BaseConstructionView):
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

        if target.kind == RailTargetType.NO_PATH:
            draw_node(self._surface, target.snapped, self._camera, color=RED)
            if self._state.construction_anchor is not None:
                draw_node(self._surface, self._state.construction_anchor.position, self._camera, color=RED)
            return

        # path preview
        screen_points = [tuple(self._camera.world_to_screen(Position(*pt))) for pt in target.found_path]
        pygame.draw.aalines(self._surface, color, False, screen_points)
        draw_node(self._surface, target.snapped, self._camera, color=color)
        draw_node(self._surface, self._state.construction_anchor.position, self._camera, color=color)
