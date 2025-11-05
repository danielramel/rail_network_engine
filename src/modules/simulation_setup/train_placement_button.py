import pygame
from core.config.paths import ICON_PATHS
from core.graphics.icon_loader import IconLoader
from core.models.geometry.position import Position
from core.config.colors import BLACK, WHITE
from core.config.settings import BUTTON_SIZE
from shared.ui.models.rectangle import RectangleUIComponent
from core.models.railway.railway_system import RailwaySystem


class TrainPlacementButton(RectangleUIComponent):
    handled_events = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL]
    def __init__(self, railway: RailwaySystem, surface: pygame.Surface):
        self.icon = IconLoader().get_icon(ICON_PATHS["TRAIN_PLACEMENT"], BUTTON_SIZE)
        _, h = surface.get_size()
        rect = pygame.Rect(BUTTON_SIZE*10 + BUTTON_SIZE//5, h - BUTTON_SIZE - BUTTON_SIZE//5, BUTTON_SIZE, BUTTON_SIZE)
        super().__init__(rect, surface)
        self._railway = railway
        
    def process_event(self, event: pygame.event) -> bool:           
        if self._rect.collidepoint(*event.screen_pos):
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                print("Rail placement button clicked")
            return True
           
        return super().process_event(event)

    def render(self, screen_pos: Position) -> None:
        pygame.draw.rect(self._surface, BLACK, self._rect, border_radius=10)

        icon_rect = self.icon.get_rect(center=self._rect.center)
        self._surface.blit(self.icon, icon_rect)
        pygame.draw.rect(self._surface, WHITE, self._rect, 2, border_radius=10)
    