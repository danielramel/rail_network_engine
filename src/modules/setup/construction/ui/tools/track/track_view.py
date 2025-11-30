from core.models.geometry.edge import Edge
from core.models.geometry.position import Position
from modules.setup.construction.models.construction_tool_view import ConstructionToolView
from core.models.geometry.position import Position
from core.config.color import Color
from shared.ui.enums.edge_action import EdgeAction
from shared.ui.utils.nodes import draw_node
from shared.ui.services.color_from_speed import color_from_speed
from shared.ui.utils.tracks import draw_track
from .track_target import find_track_target, TrackTargetType

class TrackView(ConstructionToolView):
    def render(self, world_pos: Position | None):
        if world_pos is None:
            if self._state.construction_anchor is not None:
                draw_node(self._screen, self._state.construction_anchor.node, self._camera, color=color_from_speed(self._state.track_speed))
            return

        target = find_track_target(self._railway, world_pos, self._state.construction_anchor)

        color = color_from_speed(self._state.track_speed)

        if target.kind in (TrackTargetType.ANCHOR, TrackTargetType.ANCHOR_SAME):
            draw_node(self._screen, target.node, self._camera, color)
            return
        
        if target.kind == TrackTargetType.BLOCKED:
            draw_node(self._screen, target.node, self._camera, Color.RED)
            
            if self._state.construction_anchor is not None:
                draw_node(self._screen, self._state.construction_anchor.node, self._camera, color=color)
            return

        if target.kind == TrackTargetType.NO_PATH:
            draw_node(self._screen, target.node,  self._camera, color=Color.RED)
            if self._state.construction_anchor is not None:
                draw_node(self._screen, self._state.construction_anchor.node, self._camera, color=Color.RED)
            return

        # path preview
        for line in zip(target.found_path[:-1], target.found_path[1:]):
            draw_track(self._screen, Edge(*line), camera=self._camera, edge_action=EdgeAction.SPEED, length=self._state.track_length, speed=self._state.track_speed)
        draw_node(self._screen, target.node, self._camera, color)
        draw_node(self._screen, self._state.construction_anchor.node, self._camera, color=color)
