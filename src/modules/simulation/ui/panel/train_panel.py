from core.config.config import Config
from core.models.timetable import Timetable
import pygame
from core.models.train import Train
from core.models.event import Event
from modules.simulation.models.simulation_state import SimulationState
from modules.simulation.ui.panel.schedule_selector import ScheduleSelector
from core.models.repositories.timetable_repository import TimetableRepository
from core.config.color import Color
from shared.ui.models.panel import Panel

class TrainPanel(Panel):
    _selected: bool = False
    def __init__(self, train: Train, screen: pygame.Surface, index: int, timetable_repository: TimetableRepository, simulation_state: SimulationState):
        self._train = train
        self._schedule_selector = None
        self._schedule_repository = timetable_repository
        self._state = simulation_state
        self._index = index
        self._hovered_rect: pygame.Rect | None = None
        
        super().__init__(screen, height=300, x=150 + index * 420, y=-20)
        self._init_buttons()
    
    @property
    def index(self) -> int:
        return self._index
    
    def _update_hover_state(self, screen_pos) -> None:
        """Update which button is currently hovered."""
        self._hovered_rect = None
        if screen_pos is None:
            return
        for rect in [self.close_button, self.add_schedule_button, self.change_schedule_button,
                     self.remove_schedule_button, self.startup_button, self.reverse_button]:
            if rect.collidepoint(*screen_pos):
                self._hovered_rect = rect
                break

    def render(self, screen_pos):
        self._update_hover_state(screen_pos)
        
        pygame.draw.rect(self._screen, Color.BLACK, self._rect, border_radius=8)
        border_color = self._train.schedule.color if self._train.schedule else Color.GREY if self._train.live else Color.DARKGREY
        if self._selected:
            pygame.draw.rect(self._screen, border_color, self._rect.inflate(10, 10), 7, border_radius=8)
        else:
            pygame.draw.rect(self._screen, border_color, self._rect, 4, border_radius=8)
        
        x_screen = self.instruction_font.render("X", True, Color.WHITE)
        self._screen.blit(x_screen, self._center_in_rect(x_screen, self.close_button))
        self._render_next_stop()
        self._render_speed()
        
        if self._train.live:
            color = Color.RED if self._train.speed == 0.0 else Color.DARKGREY
            self._render_button(self.shut_down_button, "Shut Down", color)
        else:
            self._render_button(self.startup_button, "Startup", Color.GREEN)
            self._render_button(self.reverse_button, "Reverse", Color.YELLOW)
            if self._train.schedule:
                self._render_button(self.change_schedule_button, "Change Schedule", Color.GREY)
                self._render_button(self.remove_schedule_button, "Remove Schedule", Color.RED)
            else:
                self._render_button(self.add_schedule_button, "Add Schedule", Color.GREY)
            
    def _on_click(self, event: Event):
        if self.close_button.collidepoint(*event.screen_pos):
            self._state.deselect_train(self._train.id)
            return

        self._state.select_train(self._train.id)
        
        if self._train.live:
            if self.shut_down_button.collidepoint(*event.screen_pos) and self._train.speed == 0.0:
                self._train.shutdown()
        else:
            if self._train.schedule:
                if self.change_schedule_button.collidepoint(*event.screen_pos):
                    self._open_schedule_selector()
                elif self.remove_schedule_button.collidepoint(*event.screen_pos):
                    self._train.remove_schedule()
            else:
                if self.add_schedule_button.collidepoint(*event.screen_pos):
                    self._open_schedule_selector()
            if self.startup_button.collidepoint(*event.screen_pos):
                self._train.start()
            elif self.reverse_button.collidepoint(*event.screen_pos):
                self._train.reverse()
                

    def _render_speed(self):
        # Speed on top left corner
        text = f"{int(self._train.speed)} km/h"
        screen = self.instruction_font.render(text, True, Color.WHITE)
        self._screen.blit(screen, (self._rect.x + self.padding, self._rect.y + self.padding))
        
        # Schedule code in top middle
        if self._train.schedule:
            code_text = self._train.schedule.timetable_code
            code_color = Color.get(self._train.schedule.color)
        else:
            code_text = "No schedule"
            code_color = Color.WHITE
        code_screen = self.instruction_font.render(code_text, True, code_color)
        code_x = self._rect.centerx - code_screen.get_width() // 2
        self._screen.blit(code_screen, (code_x, self._rect.y + self.padding))

    def _render_next_stop(self):
        if not self._train.schedule:
            return
        
        stops = self._train.schedule.get_remaining_stops()
        y_offset = self._rect.y + self.padding + 30
        first_station_color = Color.GREEN if not self._train.is_late() else Color.RED
        indicator_x = self._rect.x + self.padding + 6
        
        for i, stop in enumerate(stops[:min(3, len(stops) - 1)]):
            if i == 0:
                color = first_station_color
            else:
                color = Color.DARKGREY
                
            pygame.draw.circle(self._screen, color, (indicator_x, y_offset + 10), 5)
            
            if len(stops) <= 4 or i < min(3, len(stops)) - 1:
                pygame.draw.line(self._screen, Color.DARKGREY, 
                                (indicator_x, y_offset + 20), 
                                (indicator_x, y_offset + 45), 2)
            
            station_text = self.instruction_font.render(stop['station'], True, color)
            self._screen.blit(station_text, (indicator_x + 20, y_offset))
            
            time_surface = self.instruction_font.render(f"{stop['arrival']}  -  {stop['departure']}", True, Color.LIGHTGREY)
            self._screen.blit(time_surface, (indicator_x + 20, y_offset + 20  ))
            
            y_offset += 45
            
        
        if len(stops) > 4:
            pygame.draw.circle(self._screen, Color.DARKGREY, (indicator_x + 2, y_offset - 25), 2)
            pygame.draw.circle(self._screen, Color.DARKGREY, (indicator_x + 2, y_offset - 15), 2)
            pygame.draw.circle(self._screen, Color.DARKGREY, (indicator_x + 2, y_offset - 5), 2)
            
        indicator_color = first_station_color if len(stops) == 1 else Color.DARKGREY
        pygame.draw.circle(self._screen, indicator_color, (indicator_x, y_offset + 10), 5)
        stop = stops[-1]
        name_color = Color.WHITE if len(stops) == 1 else Color.LIGHTGREY
        station_text = self.instruction_font.render(stop['station'], True, name_color)
        self._screen.blit(station_text, (indicator_x + 20, y_offset))
        
        time_surface = self.instruction_font.render(f"{stop['arrival']}  -  {stop['departure']}", True, Color.LIGHTGREY)
        self._screen.blit(time_surface, (indicator_x + 20, y_offset + 20  ))
        

    def _render_button(self, rect, text, color):
        is_hovered = self._hovered_rect == rect
        bg_color = Color.WHITE if is_hovered and color != Color.DARKGREY else color
        pygame.draw.rect(self._screen, bg_color, rect, border_radius=5)
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

    def _on_schedule_chosen(self, timetable: Timetable, start_time: int):
        self._schedule_selector = None
        self._train.set_schedule(timetable.create_schedule(start_time))

    def _init_buttons(self):
        self.close_button = pygame.Rect(self._rect.right - 40, self._rect.top + 10, 40, 20)
        self.add_schedule_button = pygame.Rect(self._rect.centerx - 80, self._rect.bottom - 165, 160, 30)
        self.change_schedule_button = pygame.Rect(self._rect.centerx + 50, self._rect.bottom - 200, 140, 30)
        self.remove_schedule_button = pygame.Rect(self._rect.centerx + 50, self._rect.bottom - 160, 140, 30)
        self.startup_button = pygame.Rect(self._rect.centerx + 50, self._rect.bottom - 45, 140, 30)
        self.shut_down_button = self.startup_button
        self.reverse_button = pygame.Rect(self._rect.centerx - 190, self._rect.bottom - 45, 140, 30)
        
    def _center_in_rect(self, screen: pygame.Surface, rect: pygame.Rect) -> tuple[int, int]:
        return (rect.centerx - screen.get_width() // 2,
                rect.centery - screen.get_height() // 2)
        
    def deselect(self):
        self._selected = False
    
    def select(self):
        self._selected = True