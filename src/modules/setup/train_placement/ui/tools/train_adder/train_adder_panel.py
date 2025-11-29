import pygame
from core.config.color import Color
from core.config.config import Config
from core.models.event import Event
from modules.setup.train_placement.models.train_placement_state import TrainPlacementState
from shared.ui.models.panel import Panel
    
class TrainAdderPanel(Panel):    
    def __init__(self, screen: pygame.Surface, state: TrainPlacementState) -> None:
        super().__init__(screen, height=210)
        self._state = state
        self._hovered_rect: pygame.Rect | None = None
        
        self._param_ranges = {
            'car_count': (1, Config.MAX_TRAIN_CAR_COUNT, 1),
            'accel': (0.1, 2.0, 0.1),
            'max_speed': (50, 300, 10),
            'decel': (0.5, 3.0, 0.1)
        }
        
        self.title_screen = self.title_font.render("Train Placement", True, Color.YELLOW)
        
        
        self._init_layout()
       
    def _init_layout(self) -> None:
        self.title_rect = self.title_screen.get_rect(
            centerx=self._rect.centerx,
            top=self._rect.top + self.padding
        )

        controls_y = self.title_rect.bottom + 30

        # TOP ROW: max_speed, car_count
        self.max_speed_minus = pygame.Rect(self._rect.x + 20, controls_y, 30, 30)
        self.max_speed_plus  = pygame.Rect(self._rect.x + 120, controls_y, 30, 30)

        self.car_count_minus = pygame.Rect(self._rect.x + 180, controls_y, 30, 30)
        self.car_count_plus  = pygame.Rect(self._rect.x + 280, controls_y, 30, 30)

        # BOTTOM ROW: accel, decel
        controls_y += 60

        self.accel_minus = pygame.Rect(self._rect.x + 20, controls_y, 30, 30)
        self.accel_plus  = pygame.Rect(self._rect.x + 120, controls_y, 30, 30)

        self.decel_minus = pygame.Rect(self._rect.x + 180, controls_y, 30, 30)
        self.decel_plus  = pygame.Rect(self._rect.x + 280, controls_y, 30, 30)

        self.total_length_y = controls_y + 50
    
    def _update_hover_state(self, screen_pos) -> None:
        """Update which button is currently hovered."""
        self._hovered_rect = None
        if screen_pos is None:
            return
        for rect in [self.max_speed_minus, self.max_speed_plus,
                     self.car_count_minus, self.car_count_plus,
                     self.accel_minus, self.accel_plus,
                     self.decel_minus, self.decel_plus]:
            if rect.collidepoint(*screen_pos):
                self._hovered_rect = rect
                break

       
    def render(self, screen_pos) -> None:
        """Render panel with instructions."""
        super().render(screen_pos)  # background and border
        
        # Update hover state
        self._update_hover_state(screen_pos)
        
        # Title
        self._screen.blit(self.title_screen, self.title_rect)
        
        train_config = self._state.train_config
            # TOP ROW
        self._render_param_control(self.max_speed_minus, self.max_speed_plus,
                                "Max Speed", train_config.max_speed, "km/h", 'max_speed')
        self._render_param_control(self.car_count_minus, self.car_count_plus,
                                "Car Count", train_config.car_count, "", 'car_count')

        # BOTTOM ROW
        self._render_param_control(self.accel_minus, self.accel_plus,
                                "Acceleration", train_config.acceleration_in_m_s2, "m/s²", 'accel')
        self._render_param_control(self.decel_minus, self.decel_plus,
                                "Deceleration", train_config.deceleration_in_m_s2, "m/s²", 'decel')

        # Total Length
        total_length_text = f"Total Length: {train_config.total_length} m"
        total_length_screen = self.instruction_font.render(total_length_text, True, Color.WHITE)
        total_length_rect = total_length_screen.get_rect(centerx=self._rect.centerx, top=self.total_length_y)
        self._screen.blit(total_length_screen, total_length_rect)

            
    def _on_click(self, event: Event):
        if self.max_speed_minus.collidepoint(*event.screen_pos):
            self._adjust_param('max_speed', -1)
        elif self.max_speed_plus.collidepoint(*event.screen_pos):
            self._adjust_param('max_speed', 1)
        elif self.car_count_minus.collidepoint(*event.screen_pos):
            self._adjust_param('car_count', -1)
        elif self.car_count_plus.collidepoint(*event.screen_pos):
            self._adjust_param('car_count', 1)
        elif self.accel_minus.collidepoint(*event.screen_pos):
            self._adjust_param('accel', -1)
        elif self.accel_plus.collidepoint(*event.screen_pos):
            self._adjust_param('accel', 1)
        elif self.decel_minus.collidepoint(*event.screen_pos):
            self._adjust_param('decel', -1)
        elif self.decel_plus.collidepoint(*event.screen_pos):
            self._adjust_param('decel', 1)

    
    def _render_param_control(self, minus_rect: pygame.Rect, plus_rect: pygame.Rect, label, value, unit, param_key):
        y_pos = minus_rect.top
        
        text = f"{label}:"
        screen = self.instruction_font.render(text, True, Color.WHITE)
        self._screen.blit(screen, (minus_rect.x, y_pos - 18))
        
        min_val, max_val, _ = self._param_ranges[param_key]
        can_decrease = value > min_val
        self._render_small_button(minus_rect, "-", can_decrease)
        
        value_text = f"{value:.1f} {unit}" if isinstance(value, float) else f"{value} {unit}"
        value_screen = self.instruction_font.render(value_text, True, Color.YELLOW)
        center_x = (minus_rect.right + plus_rect.left) // 2
        self._screen.blit(value_screen, value_screen.get_rect(center=(center_x, minus_rect.centery)))
        
        can_increase = value < max_val
        self._render_small_button(plus_rect, "+", can_increase)

    def _render_small_button(self, rect, text, enabled):
        if enabled:
            is_hovered = self._hovered_rect == rect
            bg_color = Color.DARKGREY if is_hovered else Color.BLACK
            pygame.draw.rect(self._screen, bg_color, rect, border_radius=4)
            pygame.draw.rect(self._screen, Color.WHITE, rect, width=2, border_radius=4)
            text_screen = self.instruction_font.render(text, True, Color.WHITE)
        else:
            pygame.draw.rect(self._screen, Color.DARKGREY, rect, border_radius=4)
            text_screen = self.instruction_font.render(text, True, Color.GREY)
        
        self._screen.blit(text_screen, text_screen.get_rect(center=rect.center))

    def _adjust_param(self, param_key, direction):
        min_val, max_val, increment = self._param_ranges[param_key]
        train_config = self._state.train_config
        
        if param_key == 'car_count':
            new_val = train_config.car_count + (direction * int(increment))
            train_config.car_count = max(int(min_val), min(int(max_val), new_val))
        elif param_key == 'accel':
            new_val = train_config.acceleration_in_m_s2 + (direction * increment)
            train_config.acceleration_in_m_s2 = max(min_val, min(max_val, new_val))
        elif param_key == 'max_speed':
            new_val = train_config.max_speed + (direction * int(increment))
            train_config.max_speed = max(int(min_val), min(int(max_val), new_val))
        elif param_key == 'decel':
            new_val = train_config.deceleration_in_m_s2 + (direction * increment)
            train_config.deceleration_in_m_s2 = max(min_val, min(max_val, new_val))