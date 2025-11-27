from modules.setup.construction.models.construction_view import ConstructionView
from core.models.geometry.position import Position
from core.config.color import Color
from shared.ui.utils.signal import draw_signal
from .signal_target import find_signal_target, SignalTargetType

class SignalView(ConstructionView):
    def render(self, world_pos: Position | None):
        if world_pos is None:
            return
        target = find_signal_target(self._railway, world_pos)
        if target.pose is None:
            return

        color = Color.RED if target.kind == SignalTargetType.INVALID else Color.YELLOW
        draw_signal(self._screen, target.pose, self._camera, color=color)
