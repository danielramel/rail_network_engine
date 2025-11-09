from shared.ui.models.panel import Panel
import pygame
from modules.simulation.models.simulation_state import SimulationState
from core.config.colors import WHITE, BLACK, GREY

class SimulationPanel(Panel):
    def __init__(self, simulation_state: SimulationState, surface: pygame.Surface):
        self._state = simulation_state
        super().__init__(surface)

        self.reverse_button = pygame.Rect(
            self._rect.x + self.padding,
            self._rect.bottom - 45,
            120,
            30
        )
        self.startup_button = pygame.Rect(
            self._rect.right - self.padding - 120,
            self._rect.bottom - 45,
            120,
            30
        )

        self.font = pygame.font.SysFont(None, 26)

    def contains(self, screen_pos):
        if self._state.selected_train is None:
            return False
        return super().contains(screen_pos)

    def render(self, screen_pos):
        if self._state.selected_train is None:
            return

        super().render(screen_pos)

        train = self._state.selected_train
        speed_text = f"Speed: {train.speed:.1f} m/s"
        max_speed_text = f"Max Speed: {train.max_speed} km/h"

        speed_surface = self.font.render(speed_text, True, WHITE)
        max_speed_surface = self.font.render(max_speed_text, True, WHITE)

        self._surface.blit(speed_surface, (self._rect.x + self.padding, self._rect.y + self.padding))
        self._surface.blit(max_speed_surface, (self._rect.x + self.padding, self._rect.y + self.padding + 30))

        pygame.draw.rect(self._surface, GREY, self.reverse_button, border_radius=5)
        pygame.draw.rect(self._surface, GREY, self.startup_button, border_radius=5)

        reverse_text = self.font.render("Reverse", True, BLACK)
        startup_text = self.font.render("Startup", True, BLACK)

        self._surface.blit(
            reverse_text,
            (self.reverse_button.centerx - reverse_text.get_width() // 2,
             self.reverse_button.centery - reverse_text.get_height() // 2)
        )
        self._surface.blit(
            startup_text,
            (self.startup_button.centerx - startup_text.get_width() // 2,
             self.startup_button.centery - startup_text.get_height() // 2)
        )

    def _on_click(self, event):
        if event.is_right_click:
            return
        if self.reverse_button.collidepoint(*event.screen_pos):
            self._on_reverse_clicked()
        elif self.startup_button.collidepoint(*event.screen_pos):
            self._on_startup_clicked()

    def _on_reverse_clicked(self):
        print("reverse clicked")

    def _on_startup_clicked(self):
        print("startup clicked")
