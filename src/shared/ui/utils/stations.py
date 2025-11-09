from core.config.color import Color
from core.graphics.camera import Camera
from core.models.station import Station
import pygame
from core.config.settings import STATION_RECT_SIZE

def draw_station(surface: pygame.Surface, station: Station, camera: Camera, color=Color.PURPLE):
    width = max(1, int(round(3 * camera.scale)))
    w, h = STATION_RECT_SIZE
    rect = pygame.Rect(0, 0, w * camera.scale, h * camera.scale)
    rect.center = tuple(camera.world_to_screen(station.position))
    pygame.draw.rect(surface, Color.BLACK, rect)
    pygame.draw.rect(surface, color, rect, width)

    # Render station name text in the middle of the rect
    font = pygame.font.SysFont(None, int(rect.height * 0.6))
    text_surface = font.render(station.name, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)
