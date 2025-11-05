from shared.views.base_view import BaseView
from core.models.geometry import Position
from core.config.colors import RED, YELLOW
from shared.ui.utils import draw_signal
from modules.construction.services.signal_target import find_signal_target, SignalTargetType

class SignalView(BaseView):
    def render(self, world_pos: Position | None):
        if world_pos is None:
            return
        target = find_signal_target(self._railway, world_pos)
        if target.pose is None:
            return

        color = RED if target.kind == SignalTargetType.INVALID else YELLOW
        draw_signal(self._surface, target.pose, self._camera, color=color, offset=target.offset)
