from core.config.color import Color
from core.graphics.camera import Camera
from core.models.station import Station
import pygame
from core.config.settings import Config

def draw_station(screen: pygame.Surface, station: Station, camera: Camera, color=Color.PURPLE):
    width = max(1, int(round(3 * camera.scale)))
    w, h = Config.STATION_RECT_SIZE
    rect = pygame.Rect(0, 0, w * camera.scale, h * camera.scale)
    rect.center = tuple(camera.world_to_screen(station.position))
    pygame.draw.rect(screen, Color.BLACK, rect)
    pygame.draw.rect(screen, color, rect, width)

    # Render station name text in the middle of the rect
    font = pygame.font.SysFont(None, int(rect.height * 0.6))
    text_screen = font.render(station.name, True, color)
    text_rect = text_screen.get_rect(center=rect.center)
    screen.blit(text_screen, text_rect)
