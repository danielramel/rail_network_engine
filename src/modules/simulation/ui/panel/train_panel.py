from core.config.settings import Config
from core.models.route import Route
import pygame
from core.models.train import Train
from core.models.event import Event
from modules.simulation.ui.panel.schedule_selector import ScheduleSelector
from core.models.repositories.route_repository import RouteRepository
from core.config.color import Color
from shared.ui.models.panel import Panel
from typing import Callable

class TrainPanel(Panel):
    def __init__(self, train: Train, screen: pygame.Surface, index: int, route_repository: RouteRepository, on_close_callback: Callable):
        self._train = train
        self._schedule_selector = None
        self._schedule_repository = route_repository
        self._on_close_callback = on_close_callback
        
        super().__init__(screen, height=200, x=-420, y=20 + index * 270)
        self._init_buttons()
        
    def change_index(self, index: int):
        self._rect.y = 100 + index * 270
        self._init_buttons()

    def render(self, screen_pos):
        color = self._train.schedule.color if self._train.schedule else Config.TRAIN_LIVE_COLOR if self._train.live else Config.TRAIN_SHUTDOWN_COLOR
        super().render(screen_pos, border_color=color)
        
        x_screen = self.instruction_font.render("X", True, Color.WHITE)
        self._screen.blit(x_screen, self._center_in_rect(x_screen, self.close_button))
        self._render_next_stop()
        self._render_speed()
        
        if self._train.live:
            color = Color.GREY if self._train.speed == 0.0 else Color.DARKGREY
            self._render_button(self.stop_button, "Shut Down", color)
        else:
            label = "Change Schedule" if self._train.schedule else "Add Schedule"
            self._render_button(self.set_schedule_button, label, Color.GREY)
            self._render_button(self.startup_button, "Startup", Color.GREY)
            self._render_button(self.reverse_button, "Reverse", Color.GREY)
            if self._train.schedule:
                self._render_button(self.remove_schedule_button, "Remove Schedule", Color.GREY)
            
    def _on_click(self, event: Event):
        if self.close_button.collidepoint(*event.screen_pos):
            self._on_close_callback(self._train.id)
            
        elif self.reverse_button.collidepoint(*event.screen_pos) and not self._train.live:
            self._train.reverse()
                
        if self._train.live:
            if self.stop_button.collidepoint(*event.screen_pos) and self._train.speed == 0.0:
                self._train.shutdown()
        else:
            if self.set_schedule_button.collidepoint(*event.screen_pos):
                self._open_schedule_selector()
            elif self.remove_schedule_button.collidepoint(*event.screen_pos) and self._train.schedule:
                self._train.remove_schedule()
            elif self.startup_button.collidepoint(*event.screen_pos):
                self._train.start()

    def _render_speed(self):
        text = f"Speed: {int(self._train.speed)} km/h"
        screen = self.instruction_font.render(text, True, Color.WHITE)
        self._screen.blit(screen, (self._rect.x + self.padding, self._rect.y + self.padding))

    def _render_next_stop(self):
        if not self._train.schedule:
            return
            
        next_stop_str = self._train.schedule.get_next_stop_str()
        screen = self.instruction_font.render(next_stop_str, True, Color.WHITE)
        self._screen.blit(screen, (self._rect.x + self.padding, self._rect.y + self.padding + 30))

    def _render_button(self, rect, text, color):
        pygame.draw.rect(self._screen, color, rect, border_radius=5)
        text_screen = self.instruction_font.render(text, True, Color.BLACK)
        self._screen.blit(text_screen, self._center_in_rect(text_screen, rect))

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
            
        self._schedule_selector.window_closed.connect(lambda: setattr(self, '_schedule_selector', None))

    def _on_schedule_chosen(self, schedule: Route, start_time: int):
        self._schedule_selector = None
        self._train.set_schedule(schedule.create_schedule(start_time))

    def _init_buttons(self):
        self.close_button = pygame.Rect(self._rect.right - 30, self._rect.top + 10, 20, 20)
        self.set_schedule_button = pygame.Rect(self._rect.centerx - 60, self._rect.bottom - 125, 140, 30)
        self.remove_schedule_button = pygame.Rect(self._rect.centerx - 60, self._rect.bottom - 85, 140, 30)
        self.startup_button = pygame.Rect(self._rect.centerx + 60, self._rect.bottom - 45, 120, 30)
        self.stop_button = self.startup_button
        self.reverse_button = pygame.Rect(self._rect.centerx - 180, self._rect.bottom - 45, 120, 30)
        
    def _center_in_rect(self, screen: pygame.Surface, rect: pygame.Rect) -> tuple[int, int]:
        return (rect.centerx - screen.get_width() // 2,
                rect.centery - screen.get_height() // 2)