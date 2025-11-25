import pygame
from core.config.color import Color
from core.config.settings import Config
from modules.construction.models.construction_state import ConstructionState
from modules.construction.models.construction_panel import ConstructionToolPanel
from core.models.event import Event


class PlatformPanel(ConstructionToolPanel):
    def __init__(self, screen: pygame.Surface, state: ConstructionState) -> None:
        super().__init__(screen, state)

        self._param_ranges = {
            'platform_length': (2, Config.MAX_PLATFORM_EDGE_COUNT, 1)
        }

        self.title_screen = self.title_font.render("Platform Placement", True, Color.YELLOW)
        self.instruction1_screen = self.instruction_font.render(
            "Click on rail to place platform, then", True, Color.WHITE
        )
        self.instruction2_screen = self.instruction_font.render(
            "connect it to already existing station.", True, Color.WHITE
        )

        self.length_label_screen = self.instruction_font.render("Length:", True, Color.WHITE)

        self.minus_text = self.instruction_font.render("-", True, Color.WHITE)
        self.plus_text = self.instruction_font.render("+", True, Color.WHITE)

        self.button_size = 32
        self._init_layout()

    def _init_layout(self):
        self.title_rect = self.title_screen.get_rect(
            centerx=self._rect.centerx,
            top=self._rect.top + self.padding
        )

        self.instruction1_rect = self.instruction1_screen.get_rect(
            left=self._rect.left + self.padding,
            top=self.title_rect.bottom + 20
        )

        self.instruction2_rect = self.instruction2_screen.get_rect(
            left=self._rect.left + self.padding,
            top=self.instruction1_rect.bottom + 5
        )

        self.length_label_rect = self.length_label_screen.get_rect(
            left=self._rect.left + self.padding,
            top=self.instruction2_rect.bottom + 25
        )

        y = self.length_label_rect.top - 6
        minus_x = self.length_label_rect.right + 20
        plus_x = minus_x + self.button_size + 90

        self.length_minus_rect = pygame.Rect(minus_x, y, self.button_size, self.button_size)
        self.length_plus_rect = pygame.Rect(plus_x, y, self.button_size, self.button_size)

        self.length_value_center = (
            (self.length_minus_rect.right + self.length_plus_rect.left) // 2,
            self.length_minus_rect.centery
        )

    def _get_value(self, key):
        return self._state.platform_edge_count

    def _set_value(self, key, value):
        self._state.platform_edge_count = value

    def _adjust_param(self, key, direction):
        min_val, max_val, inc = self._param_ranges[key]
        val = self._get_value(key)
        new_val = max(min_val, min(max_val, val + direction * inc))
        self._set_value(key, new_val)

    def _render_small_button(self, rect, text, enabled):
        if enabled:
            pygame.draw.rect(self._screen, Color.BLACK, rect, border_radius=4)
            pygame.draw.rect(self._screen, Color.WHITE, rect, width=2, border_radius=4)
            txt = self.instruction_font.render(text, True, Color.WHITE)
        else:
            pygame.draw.rect(self._screen, Color.DARKGREY, rect, border_radius=4)
            txt = self.instruction_font.render(text, True, Color.GREY)

        self._screen.blit(txt, txt.get_rect(center=rect.center))

    def _render_param_control(self, minus_rect: pygame.Rect, plus_rect: pygame.Rect, label, value, key):
        y = minus_rect.top
        label_screen = self.instruction_font.render(label + ":", True, Color.WHITE)
        self._screen.blit(label_screen, (minus_rect.x - 70, minus_rect.centery-7)) # this is different than in train_panel.py

        min_val, max_val, _ = self._param_ranges[key]

        can_decrease = value > min_val
        can_increase = value < max_val

        self._render_small_button(minus_rect, "-", can_decrease)
        self._render_small_button(plus_rect, "+", can_increase)

        value_text = f"{value * Config.SHORT_SECTION_LENGTH} m"
        val_screen = self.instruction_font.render(value_text, True, Color.YELLOW)
        self._screen.blit(val_screen, val_screen.get_rect(center=self.length_value_center))

    def render(self, screen_pos):
        super().render(screen_pos)

        self._screen.blit(self.title_screen, self.title_rect)
        self._screen.blit(self.instruction1_screen, self.instruction1_rect)
        self._screen.blit(self.instruction2_screen, self.instruction2_rect)

        val = self._state.platform_edge_count

        self._render_param_control(
            self.length_minus_rect,
            self.length_plus_rect,
            "Length",
            val,
            "platform_length"
        )

    def _on_click(self, event: Event) -> bool:
        if not event.is_left_click:
            return self._rect.collidepoint(*event.screen_pos)

        if self.length_minus_rect.collidepoint(*event.screen_pos):
            self._adjust_param("platform_length", -1)
            return True

        if self.length_plus_rect.collidepoint(*event.screen_pos):
            self._adjust_param("platform_length", 1)
            return True

        return self._rect.collidepoint(*event.screen_pos)
