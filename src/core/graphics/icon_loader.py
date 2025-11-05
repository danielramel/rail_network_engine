import pygame
from core.config.colors import WHITE

class IconLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._cache = {}


    def get_icon(self, path: str, size: int) -> pygame.Surface:
        """Scale and color an icon, caching the result. Size is ignored if already cached."""
        if path in self._cache:
            return self._cache[path]
        
        icon = pygame.image.load(path).convert_alpha()
        icon = pygame.transform.scale(icon, (int(size*0.8), int(size*0.8)))

        colored_icon = pygame.Surface(icon.get_size(), pygame.SRCALPHA)
        colored_icon.fill(WHITE)

        alpha_mask = pygame.surfarray.pixels_alpha(icon)
        pygame.surfarray.pixels_alpha(colored_icon)[:] = alpha_mask

        self._cache[path] = colored_icon
        return colored_icon
