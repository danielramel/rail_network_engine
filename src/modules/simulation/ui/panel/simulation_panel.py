from core.models.schedule import Schedule
import pygame
from modules.simulation.models.simulation_state import SimulationState
from core.models.event import Event
from modules.simulation.ui.panel.schedule_selector import ScheduleSelector
from core.models.repositories.schedule_repository import ScheduleRepository
from shared.ui.models.panel import Panel
from core.config.color import Color

class TrainPanel(Panel):
    def __init__(self, simulation_state: SimulationState, surface: pygame.Surface, schedule_repository: ScheduleRepository):
        self._state = simulation_state
        self._select_schedule_window = None
        self._schedule_repository = schedule_repository
        super().__init__(surface)

        self.startup_button = pygame.Rect(
            self._rect.centerx - 60,
            self._rect.bottom - 85,
            120,
            30
        )
        
        self.schedule_button = self.startup_button
        
        self.shutdown_button = pygame.Rect(
            self._rect.centerx + 60,
            self._rect.bottom - 45,
            120,
            30
        )

        self.reverse = pygame.Rect(
            self._rect.centerx - 180,
            self._rect.bottom - 45,
            120,
            30
        )

        

        self.close_button = pygame.Rect(
            self._rect.right - 35,
            self._rect.top + 5,
            30,
            30
        )


    def render(self, screen_pos):
        train = self._state.selected_train
        if train is None:
            return

        super().render(screen_pos)

        x_surface = self.instruction_font.render("X", True, Color.WHITE)
        self._surface.blit(
            x_surface,
            (self.close_button.centerx - x_surface.get_width() // 2,
             self.close_button.centery - x_surface.get_height() // 2)
        )

        if not train.is_live:
            pygame.draw.rect(self._surface, Color.GREY, self.startup_button, border_radius=5)
            label_surface = self.instruction_font.render("Startup", True, Color.BLACK)
            self._surface.blit(
                label_surface,
                (self.startup_button.centerx - label_surface.get_width() // 2,
                 self.startup_button.centery - label_surface.get_height() // 2)
            )
            return

        speed_text = f"Speed: {train.speed*3.6:.1f} km/h"
        speed_surface = self.instruction_font.render(speed_text, True, Color.WHITE)
        self._surface.blit(speed_surface, (self._rect.x + self.padding, self._rect.y + self.padding))

        if train.timetable:
            next_stop = train.timetable.get_next_stop(0)
            if next_stop is None:
                next_station_surface = self.instruction_font.render("No more stops.", True, Color.WHITE)
                self._surface.blit(next_station_surface, (self._rect.x + self.padding, self._rect.y + self.padding + 30))
            else:
                next_station_text = f"Next: {next_stop['station'].id}; {next_stop['arrival_time']} min"
                next_station_surface = self.instruction_font.render(next_station_text, True, Color.WHITE)
                self._surface.blit(next_station_surface, (self._rect.x + self.padding, self._rect.y + self.padding + 30))

        # Always show schedule button (Set Schedule or Change Schedule)
        schedule_label = "Change Schedule" if train.timetable else "Add Schedule"
        pygame.draw.rect(self._surface, Color.GREY, self.schedule_button, border_radius=5)
        schedule_text = self.instruction_font.render(schedule_label, True, Color.BLACK)
        self._surface.blit(
            schedule_text,
            (self.schedule_button.centerx - schedule_text.get_width() // 2,
             self.schedule_button.centery - schedule_text.get_height() // 2)
        )


        pygame.draw.rect(self._surface, Color.GREY, self.reverse, border_radius=5)
        direction_label = self.instruction_font.render("Reverse (R)", True, Color.BLACK)
        self._surface.blit(
            direction_label,
            (self.reverse.centerx - direction_label.get_width() // 2,
                self.reverse.centery - direction_label.get_height() // 2)
        )

        button_color = Color.DARKGREY if train.speed != 0.0 else Color.GREY
        pygame.draw.rect(self._surface, button_color, self.shutdown_button, border_radius=5)
        label_surface = self.instruction_font.render("Shut Down", True, Color.BLACK)
        self._surface.blit(
            label_surface,
            (self.shutdown_button.centerx - label_surface.get_width() // 2,
             self.shutdown_button.centery - label_surface.get_height() // 2)
        )

    def contains(self, screen_pos):
        if self._state.selected_train is None:
            return False
        return super().contains(screen_pos)

    def _on_click(self, event: Event):
        train = self._state.selected_train
        if self.close_button.collidepoint(*event.screen_pos):
            self._state.selected_train = None
        elif train.is_live and self.schedule_button.collidepoint(*event.screen_pos):
            self._on_set_schedule_clicked()
        elif not train.is_live and self.startup_button.collidepoint(*event.screen_pos):
            train.start()
        elif train.is_live and train.speed == 0.0 and self.reverse.collidepoint(*event.screen_pos):
            pass  # TODO: Implement reverse direction logic
        elif train.is_live and train.speed == 0.0 and self.shutdown_button.collidepoint(*event.screen_pos):
            train.shutdown()

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