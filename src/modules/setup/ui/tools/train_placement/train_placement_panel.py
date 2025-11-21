import pygame
from core.config.color import Color
from core.models.event import Event
from modules.setup.models.setup_state import SetupState
from shared.ui.models.panel import Panel
    
class TrainPlacementPanel(Panel):
    """Signal placement panel with instructions."""
    
    def __init__(self, surface: pygame.Surface, state: SetupState) -> None:
        super().__init__(surface, width=500, height=200)
        self._state = state
        
        self._param_ranges = {
            'car_count': (1, 10, 1),
            'car_length': (10.0, 40.0, 0.5),
            'car_gap': (0, 5, 1),
            'accel': (0.1, 2.0, 0.1),
            'max_speed': (50, 200, 10),
            'decel': (0.5, 3.0, 0.1)
        }
        
        # Pre-render static text
        self.title_surface = self.title_font.render("Train Placement", True, Color.YELLOW)
        self.instruction1_surface = self.instruction_font.render(
            "Click on rail to place train.", True, Color.WHITE
        )
        
        # Calculate and store all layout rects
        self._init_layout()
       
    def _init_layout(self) -> None:
        """Compute and persist all rects for layout."""
        # Title position
        self.title_rect = self.title_surface.get_rect(
            centerx=self._rect.centerx, 
            top=self._rect.top + self.padding
        )
        
        # Instruction positions
        self.instruction1_rect = self.instruction1_surface.get_rect(
            left=self._rect.left + self.padding,
            top=self.title_rect.bottom + 20
        )
        
        # Parameter controls
        # Top row: max_speed, accel, decel
        controls_y = self.instruction1_rect.bottom + 30
        
        self.max_speed_minus = pygame.Rect(self._rect.x + 20, controls_y, 30, 30)
        self.max_speed_plus = pygame.Rect(self._rect.x + 120, controls_y, 30, 30)
        
        self.accel_minus = pygame.Rect(self._rect.x + 180, controls_y, 30, 30)
        self.accel_plus = pygame.Rect(self._rect.x + 280, controls_y, 30, 30)
        
        self.decel_minus = pygame.Rect(self._rect.x + 340, controls_y, 30, 30)
        self.decel_plus = pygame.Rect(self._rect.x + 440, controls_y, 30, 30)
        
        # Bottom row: car_count, car_length, car_gap
        controls_y += 60
        
        self.car_count_minus = pygame.Rect(self._rect.x + 20, controls_y, 30, 30)
        self.car_count_plus = pygame.Rect(self._rect.x + 120, controls_y, 30, 30)
        
        self.car_length_minus = pygame.Rect(self._rect.x + 180, controls_y, 30, 30)
        self.car_length_plus = pygame.Rect(self._rect.x + 280, controls_y, 30, 30)
        
        self.car_gap_minus = pygame.Rect(self._rect.x + 340, controls_y, 30, 30)
        self.car_gap_plus = pygame.Rect(self._rect.x + 440, controls_y, 30, 30)
       
    def render(self, screen_pos) -> None:
        """Render panel with instructions."""
        super().render(screen_pos)  # background and border

        # Title
        self._surface.blit(self.title_surface, self.title_rect)
        
        # Instructions
        self._surface.blit(self.instruction1_surface, self.instruction1_rect)
        
        # Parameter controls
        train_config = self._state.train_config
        # Top row
        self._render_param_control(self.max_speed_minus, self.max_speed_plus, "Max Speed", 
                                   train_config.max_speed, "km/h", 'max_speed')
        self._render_param_control(self.accel_minus, self.accel_plus, "Accel", 
                                   train_config.acceleration, "m/s²", 'accel')
        self._render_param_control(self.decel_minus, self.decel_plus, "Decel", 
                                   train_config.deceleration, "m/s²", 'decel')
        # Bottom row
        self._render_param_control(self.car_count_minus, self.car_count_plus, "Car Count", 
                                   train_config.car_count, "", 'car_count')
        self._render_param_control(self.car_length_minus, self.car_length_plus, "Car Length", 
                                   train_config.car_length, "m", 'car_length')
        self._render_param_control(self.car_gap_minus, self.car_gap_plus, "Car Gap", 
                                   train_config.car_gap, "m", 'car_gap')
    
    def _on_click(self, event: Event):
        if self.car_count_minus.collidepoint(*event.screen_pos):
            self._adjust_param('car_count', -1)
        elif self.car_count_plus.collidepoint(*event.screen_pos):
            self._adjust_param('car_count', 1)
        elif self.car_length_minus.collidepoint(*event.screen_pos):
            self._adjust_param('car_length', -1)
        elif self.car_length_plus.collidepoint(*event.screen_pos):
            self._adjust_param('car_length', 1)
        elif self.car_gap_minus.collidepoint(*event.screen_pos):
            self._adjust_param('car_gap', -1)
        elif self.car_gap_plus.collidepoint(*event.screen_pos):
            self._adjust_param('car_gap', 1)
        elif self.accel_minus.collidepoint(*event.screen_pos):
            self._adjust_param('accel', -1)
        elif self.accel_plus.collidepoint(*event.screen_pos):
            self._adjust_param('accel', 1)
        elif self.max_speed_minus.collidepoint(*event.screen_pos):
            self._adjust_param('max_speed', -1)
        elif self.max_speed_plus.collidepoint(*event.screen_pos):
            self._adjust_param('max_speed', 1)
        elif self.decel_minus.collidepoint(*event.screen_pos):
            self._adjust_param('decel', -1)
        elif self.decel_plus.collidepoint(*event.screen_pos):
            self._adjust_param('decel', 1)
    
    def _render_param_control(self, minus_rect: pygame.Rect, plus_rect: pygame.Rect, label, value, unit, param_key):
        y_pos = minus_rect.top
        
        text = f"{label}:"
        surface = self.instruction_font.render(text, True, Color.WHITE)
        self._surface.blit(surface, (minus_rect.x, y_pos - 18))
        
        min_val, max_val, _ = self._param_ranges[param_key]
        can_decrease = value > min_val
        self._render_small_button(minus_rect, "-", can_decrease)
        
        value_text = f"{value:.1f} {unit}" if isinstance(value, float) else f"{value} {unit}"
        value_surface = self.instruction_font.render(value_text, True, Color.YELLOW)
        center_x = (minus_rect.right + plus_rect.left) // 2
        self._surface.blit(value_surface, value_surface.get_rect(center=(center_x, minus_rect.centery)))
        
        can_increase = value < max_val
        self._render_small_button(plus_rect, "+", can_increase)

    def _render_small_button(self, rect, text, enabled):
        if enabled:
            pygame.draw.rect(self._surface, Color.BLACK, rect, border_radius=4)
            pygame.draw.rect(self._surface, Color.WHITE, rect, width=2, border_radius=4)
            text_surface = self.instruction_font.render(text, True, Color.WHITE)
        else:
            pygame.draw.rect(self._surface, Color.DARKGREY, rect, border_radius=4)
            text_surface = self.instruction_font.render(text, True, Color.GREY)
        
        self._surface.blit(text_surface, text_surface.get_rect(center=rect.center))

    def _adjust_param(self, param_key, direction):
        min_val, max_val, increment = self._param_ranges[param_key]
        train_config = self._state.train_config
        
        if param_key == 'car_count':
            new_val = train_config.car_count + (direction * int(increment))
            train_config.car_count = max(int(min_val), min(int(max_val), new_val))
        elif param_key == 'car_length':
            new_val = train_config.car_length + (direction * increment)
            train_config.car_length = max(min_val, min(max_val, new_val))
        elif param_key == 'car_gap':
            new_val = train_config.car_gap + (direction * int(increment))
            train_config.car_gap = max(int(min_val), min(int(max_val), new_val))
        elif param_key == 'accel':
            new_val = train_config.acceleration + (direction * increment)
            train_config.acceleration = max(min_val, min(max_val, new_val))
        elif param_key == 'max_speed':
            new_val = train_config.max_speed + (direction * int(increment))
            train_config.max_speed = max(int(min_val), min(int(max_val), new_val))
        elif param_key == 'decel':
            new_val = train_config.deceleration + (direction * increment)
            train_config.deceleration = max(min_val, min(max_val, new_val))