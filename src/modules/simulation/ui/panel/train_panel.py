from core.models.schedule import Schedule
import pygame
from core.models.train import Train
from core.models.event import Event
from modules.simulation.ui.panel.schedule_selector import ScheduleSelector
from core.models.repositories.schedule_repository import ScheduleRepository
from core.config.color import Color
from shared.ui.models.panel import Panel
from typing import Callable

class TrainPanel(Panel):
    def __init__(self, train: Train, surface: pygame.Surface, index: int, 
                 schedule_repository: ScheduleRepository, on_close_callback: Callable):
        self._train = train
        self._schedule_selector = None
        self._schedule_repository = schedule_repository
        self._on_close_callback = on_close_callback
        
        self._param_ranges = {
            'accel': (0.1, 2.0, 0.1), #TODO set everything to zero
            'speed': (50, 200, 10),
            'decel': (0.5, 3.0, 0.1)
        }
        
        rect = pygame.Rect(surface.get_width() - 420, 20 + index * 180, 400, 250)
        super().__init__(surface, rect)
        self._init_buttons()
        
    def change_index(self, index: int):
        self._rect.y = 20 + index * 270
        self._init_buttons()

    def render(self, screen_pos):
        super().render(screen_pos)
        
        x_surface = self.instruction_font.render("X", True, Color.WHITE)
        self._surface.blit(x_surface, self._center_in_rect(x_surface, self.close_button))
        
        if self._train.is_live:
            self._render_speed()
            self._render_next_stop()
            
            label = "Change Schedule" if self._train.timetable else "Add Schedule"
            self._render_button(self.schedule_button, label, Color.GREY)
            
            color = Color.DARKGREY if self._train._is_shutting_down else Color.GREY
            self._render_button(self.stop_button, "Shut Down", color)
        else:
            self._render_param_control(self.accel_minus, self.accel_plus, "Accel", 
                                       self._train.acceleration, "m/s²", 'accel')
            self._render_param_control(self.speed_minus, self.speed_plus, "Max Speed", 
                                       self._train.max_speed, "km/h", 'speed')
            self._render_param_control(self.decel_minus, self.decel_plus, "Decel", 
                                       self._train.deceleration, "m/s²", 'decel')
            self._render_button(self.startup_button, "Startup", Color.GREY)
            self._render_button(self.reverse_button, "Reverse (R)", Color.GREY)
            
    def _on_click(self, event: Event):
        if self.close_button.collidepoint(*event.screen_pos):
            self._on_close_callback(self._train.id)
            return
            
        if self._train.is_live:
            if self.schedule_button.collidepoint(*event.screen_pos):
                self._open_schedule_selector()
            elif self.stop_button.collidepoint(*event.screen_pos):
                self._train.initiate_shutdown()
        else:
            if self.accel_minus.collidepoint(*event.screen_pos):
                self._adjust_param('accel', -1)
            elif self.accel_plus.collidepoint(*event.screen_pos):
                self._adjust_param('accel', 1)
            elif self.speed_minus.collidepoint(*event.screen_pos):
                self._adjust_param('speed', -1)
            elif self.speed_plus.collidepoint(*event.screen_pos):
                self._adjust_param('speed', 1)
            elif self.decel_minus.collidepoint(*event.screen_pos):
                self._adjust_param('decel', -1)
            elif self.decel_plus.collidepoint(*event.screen_pos):
                self._adjust_param('decel', 1)
            elif self.startup_button.collidepoint(*event.screen_pos):
                self._train.start()
            elif self.reverse_button.collidepoint(*event.screen_pos):
                self._train.reverse()

    def _render_speed(self):
        text = f"Speed: {self._train.speed * 3.6:.1f} km/h"
        surface = self.instruction_font.render(text, True, Color.WHITE)
        self._surface.blit(surface, (self._rect.x + self.padding, self._rect.y + self.padding))

    def _render_next_stop(self):
        if not self._train.timetable:
            return
            
        next_stop = self._train.timetable.get_next_stop(0)
        text = "No more stops." if next_stop is None else f"Next: {next_stop['station'].id}; {next_stop['arrival_time']} min"
        surface = self.instruction_font.render(text, True, Color.WHITE)
        self._surface.blit(surface, (self._rect.x + self.padding, self._rect.y + self.padding + 30))

    def _render_button(self, rect, text, color):
        pygame.draw.rect(self._surface, color, rect, border_radius=5)
        text_surface = self.instruction_font.render(text, True, Color.BLACK)
        self._surface.blit(text_surface, self._center_in_rect(text_surface, rect))

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
        
        if param_key == 'accel':
            new_val = self._train.acceleration + (direction * increment)
            self._train.acceleration = max(min_val, min(max_val, new_val))
        elif param_key == 'speed':
            new_val = self._train.max_speed + (direction * int(increment))
            self._train.max_speed = max(int(min_val), min(int(max_val), new_val))
        elif param_key == 'decel':
            new_val = self._train.deceleration + (direction * increment)
            self._train.deceleration = max(min_val, min(max_val, new_val))

    def _open_schedule_selector(self):
        if self._schedule_selector is None:
            self._schedule_selector = ScheduleSelector(self._schedule_repository.all())
            self._schedule_selector.schedule_chosen.connect(self._on_schedule_chosen)
            self._schedule_selector.show()
        else:
            if self._schedule_selector.isMinimized():
                self._schedule_selector.showNormal()
            self._schedule_selector.raise_()
            self._schedule_selector.activateWindow()

    def _on_schedule_chosen(self, schedule: Schedule, start_time: int):
        self._schedule_selector = None
        self._train.set_timetable(schedule.create_timetable(start_time))

    def _init_buttons(self):
        self.close_button = pygame.Rect(self._rect.right - 30, self._rect.top + 10, 20, 20)
        self.schedule_button = pygame.Rect(self._rect.centerx - 60, self._rect.bottom - 85, 120, 30)
        self.startup_button = pygame.Rect(self._rect.centerx + 60, self._rect.bottom - 45, 120, 30)
        self.stop_button = self.startup_button
        self.reverse_button = pygame.Rect(self._rect.centerx - 180, self._rect.bottom - 45, 120, 30)
        
        controls_y = self._rect.top + 30
        self.accel_minus = pygame.Rect(self._rect.x + 20, controls_y, 30, 30)
        self.accel_plus = pygame.Rect(self._rect.x + 120, controls_y, 30, 30)
        
        controls_y += 60
        self.speed_minus = pygame.Rect(self._rect.x + 20, controls_y, 30, 30)
        self.speed_plus = pygame.Rect(self._rect.x + 120, controls_y, 30, 30)
        
        controls_y += 60
        self.decel_minus = pygame.Rect(self._rect.x + 20, controls_y, 30, 30)
        self.decel_plus = pygame.Rect(self._rect.x + 120, controls_y, 30, 30)
    def _center_in_rect(self, surface, rect):
        return (rect.centerx - surface.get_width() // 2,
                rect.centery - surface.get_height() // 2)