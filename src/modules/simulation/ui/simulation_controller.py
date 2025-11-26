from core.models.geometry.position import Position
from core.models.railway.railway_system import RailwaySystem
from modules.simulation.models.simulation_state import SimulationState
from modules.simulation.ui.simulation_target import SimulationTargetType, find_simulation_target
from shared.ui.models.full_screen_ui_component import FullScreenUIComponent
from shared.ui.models.clickable_ui_component import ClickableUIComponent
from modules.simulation.ui.simulation_view import SimulationView
from core.graphics.graphics_context import GraphicsContext
from core.models.event import Event
import pygame


class SimulationController(ClickableUIComponent, FullScreenUIComponent):
    handled_events = [pygame.MOUSEBUTTONUP]
    def __init__(self, railway: RailwaySystem, simulation_state: SimulationState, graphics: GraphicsContext):
        self.view = SimulationView(railway, simulation_state, graphics)
        self._state = simulation_state
        self._railway = railway
        self._graphics = graphics


    def _on_click(self, click: Event) -> None:
        if click.is_right_click and self._state.selected_signal is not None:
            self._state.selected_signal = None
            return
        
        target = find_simulation_target(self._railway, click.world_pos)
        
        if target.kind == SimulationTargetType.NODE:
            is_blocked = bool(self._railway.graph.get_node_attr(target.node, "blocked"))
            if click.is_right_click and is_blocked:
                self._railway.graph.unblock_node(target.node)
            elif click.is_left_click and not is_blocked:
                self._railway.graph.block_node(target.node)
        
        elif target.kind ==  SimulationTargetType.TRAIN:
            self._state.select_train(target.train_id)
            
        elif target.kind == SimulationTargetType.SIGNAL:
            # click on signal
            if click.is_right_click:
                self._railway.signalling.drop_signal(target.signal)
                return
            
            
            if self._state.selected_signal is None:
                self._state.selected_signal = target.signal
                return
            
            
            shift_pressed = bool(pygame.key.get_mods() & pygame.KMOD_SHIFT)
            if self._state.selected_signal.next_signal is not None and not shift_pressed:
                self._graphics.alert_component.show_alert("Selected signal is already connected to another signal.")
                self._state.selected_signal = None
                return
            
            
            if shift_pressed:
                message = self._railway.signalling.auto_connect_signals(self._state.selected_signal, target.signal)
                if message is None:
                    self._state.selected_signal = None
                else:
                    self._graphics.alert_component.show_alert(message)
            else:
                successful = self._railway.signalling.connect_signals(self._state.selected_signal, target.signal)
                if successful:
                    self._state.selected_signal = None
                else:
                    self._graphics.alert_component.show_alert("Failed to connect signals: Path is blocked or invalid.")

            
            
    def render(self, screen_pos: Position | None):
        world_pos = None if screen_pos is None else self._graphics.camera.screen_to_world(screen_pos)
        self.view.render(world_pos)

    
    def tick(self):
        if self._state.time_control.paused:
            return
        self._state.tick()
        for _ in range(self._state.time_control.mode.value):
            self._railway.tick()