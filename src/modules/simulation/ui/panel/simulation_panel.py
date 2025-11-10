from core.models.schedule import Schedule
import pygame
from modules.simulation.models.simulation_state import SimulationState
from core.models.event import Event
from modules.simulation.ui.panel.schedule_selector import ScheduleSelector
from core.models.repositories.schedule_repository import ScheduleRepository
from shared.ui.models.panel import Panel
from core.config.color import Color

class SimulationPanel(Panel):
    def __init__(self, simulation_state: SimulationState, surface: pygame.Surface, schedule_repository: ScheduleRepository):
        self._state = simulation_state
        self._select_schedule_window = None
        self._schedule_repository = schedule_repository
        super().__init__(surface)

        self.schedule_button = pygame.Rect(
            self._rect.centerx - 60,
            self._rect.bottom - 45,
            120,
            30
        )

        self.train_button = pygame.Rect(
            self._rect.centerx - 60,
            self._rect.bottom - 85,
            120,
            30
        )

    def render(self, screen_pos):
        if self._state.selected_train is None:
            return

        super().render(screen_pos)

        train = self._state.selected_train
        speed_text = f"Speed: {train.speed:.1f} m/s"
        max_speed_text = f"Max Speed: {train.max_speed} km/h"

        speed_surface = self.instruction_font.render(speed_text, True, Color.WHITE)
        max_speed_surface = self.instruction_font.render(max_speed_text, True, Color.WHITE)

        self._surface.blit(speed_surface, (self._rect.x + self.padding, self._rect.y + self.padding))
        self._surface.blit(max_speed_surface, (self._rect.x + self.padding, self._rect.y + self.padding + 30))

        # timetable or set schedule
        if train.timetable:
            next_stop = train.timetable.get_next_stop(0)
            if next_stop:
                next_station_text = f"Next: {next_stop['station'].id}; {next_stop['arrival_time']} min"
                next_station_surface = self.instruction_font.render(next_station_text, True, Color.WHITE)
                self._surface.blit(next_station_surface, (self._rect.x + self.padding, self._rect.y + self.padding + 60))
        else:
            pygame.draw.rect(self._surface, Color.GREY, self.schedule_button, border_radius=5)
            schedule_text = self.instruction_font.render("Set Schedule", True, Color.BLACK)
            self._surface.blit(
                schedule_text,
                (self.schedule_button.centerx - schedule_text.get_width() // 2,
                 self.schedule_button.centery - schedule_text.get_height() // 2)
            )

        # start/shutdown train button
        button_label = "Start Train" if not train.is_live else "Shut Down Train"
        pygame.draw.rect(self._surface, Color.GREY, self.train_button, border_radius=5)
        label_surface = self.instruction_font.render(button_label, True, Color.BLACK)
        self._surface.blit(
            label_surface,
            (self.train_button.centerx - label_surface.get_width() // 2,
             self.train_button.centery - label_surface.get_height() // 2)
        )

    def contains(self, screen_pos):
        if self._state.selected_train is None:
            return False
        return super().contains(screen_pos)

    def _on_click(self, event: Event):
        if self.schedule_button.collidepoint(*event.screen_pos):
            self._on_set_schedule_clicked()
        elif self.train_button.collidepoint(*event.screen_pos):
            self._on_train_button_clicked()

    def _on_set_schedule_clicked(self):
        if self._select_schedule_window is None:
            self._select_schedule_window = ScheduleSelector(self._schedule_repository.all())
            self._select_schedule_window.schedule_chosen.connect(self._on_schedule_chosen)
            self._select_schedule_window.show()
        else:
            if self._select_schedule_window.isMinimized():
                self._select_schedule_window.showNormal()
            self._select_schedule_window.raise_()
            self._select_schedule_window.activateWindow()

    def _on_schedule_chosen(self, schedule: Schedule, start_time: int):
        self._select_schedule_window = None
        self._state.selected_train.set_timetable(schedule.create_timetable(start_time))

    def _on_train_button_clicked(self):
        train = self._state.selected_train
        if not train.is_live:
            train.start()
        else:
            train.shutdown()
