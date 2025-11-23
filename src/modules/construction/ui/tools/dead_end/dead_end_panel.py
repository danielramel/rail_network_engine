import pygame
from core.config.color import Color
from core.config.settings import Config
from modules.construction.models.construction_state import ConstructionState
from modules.construction.models.construction_panel import ConstructionToolPanel
from core.models.event import Event


class DeadEndPanel(ConstructionToolPanel):
    def __init__(self, screen: pygame.Surface, state: ConstructionState) -> None:
        super().__init__(screen, state)
        self.title_screen = self.title_font.render("Dead End Placement", True, Color.YELLOW)
        self.instruction_screen = self.instruction_font.render(
            "Click on end of rail to place dead end.", True, Color.WHITE
        )
        self.button_size = 32
        self._init_layout()

    def _init_layout(self):
        self.title_rect = self.title_screen.get_rect(
            centerx=self._rect.centerx,
            top=self._rect.top + self.padding
        )

        self.instruction_rect = self.instruction_screen.get_rect(
            left=self._rect.left + self.padding,
            top=self.title_rect.bottom + 20
        )

    def render(self, screen_pos):
        super().render(screen_pos)

        self._screen.blit(self.title_screen, self.title_rect)
        self._screen.blit(self.instruction_screen, self.instruction_rect)