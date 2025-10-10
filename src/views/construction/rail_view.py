import pygame
from views.construction.base_construction_view import BaseConstructionView
from models.geometry import Position
from config.colors import RED
from ui.utils import draw_node, color_from_speed
from services.construction.rail_target import find_rail_target

class RailView(BaseConstructionView):
    def render(self, world_pos: Position):
        target = find_rail_target(self._map, world_pos, self._construction_state.construction_anchor)

        if target.kind == 'blocked':
            draw_node(self._surface, target.snapped, self._camera, color=RED)
            if self._construction_state.construction_anchor is not None:
                draw_node(self._surface, self._construction_state.construction_anchor.position, self._camera, color=RED)
            return

        color = color_from_speed(self._construction_state.track_speed)

        if target.kind in ('node', 'anchor_same'):
            draw_node(self._surface, target.snapped, self._camera, color=color)
            return

        if target.kind == 'no_path':
            draw_node(self._surface, target.snapped, self._camera, color=RED)
            draw_node(self._surface, self._construction_state.construction_anchor.position, self._camera, color=RED)
            return

        # path preview
        screen_points = [tuple(self._camera.world_to_screen(Position(*pt))) for pt in target.found_path]
        pygame.draw.aalines(self._surface, color, False, screen_points)
        draw_node(self._surface, target.snapped, self._camera, color=color)
        draw_node(self._surface, self._construction_state.construction_anchor.position, self._camera, color=color)
