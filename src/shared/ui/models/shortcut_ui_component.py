import pygame
from shared.ui.models.ui_component import UIComponent
from typing import Callable

class ShortcutUIComponent(UIComponent):
    _shortcuts: dict[tuple[int, bool], Callable] = {}

    def dispatch_event(self, event):
        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            ctrl_pressed = bool(mods & pygame.KMOD_CTRL)
            key_combo = (event.key, ctrl_pressed)

            if key_combo in self._shortcuts:
                self._shortcuts[key_combo]()
                return True
            return False
        
        return super().dispatch_event(event)
