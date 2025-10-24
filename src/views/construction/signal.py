import pygame
from views.construction.base_construction_view import BaseConstructionView
from models.geometry import Position
from config.colors import RED, YELLOW
from ui.utils import draw_signal
from services.construction.signal_target import find_signal_target, SignalTargetType

class SignalView(BaseConstructionView):
    def render(self, world_pos: Position | None):
        if world_pos is None:
            return
        target = find_signal_target(self._railway, world_pos)
        if target.preview_pose is None:
            return

        color = RED if target.kind == SignalTargetType.INVALID else YELLOW
        draw_signal(self._surface, target.preview_pose, self._camera, color=color, offset=target.offset)
