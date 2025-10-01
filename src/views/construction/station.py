import pygame
from graphics.camera import Camera
from models.geometry import Position
from models.map import RailMap
from models.construction import ConstructionState
from ui_elements.draw_utils import draw_station
from config.colors import RED, YELLOW


def render_station_preview(surface : pygame.Surface, world_pos: Position, map: RailMap, camera: Camera):
    snapped = world_pos.snap_to_grid()

    color = YELLOW
    if any(snapped.within_station_rect(node_pos) for node_pos in map.graph.nodes):
        color = RED
    elif any(snapped.station_rect_overlaps(station_pos) for station_pos in map.get_all_stations().keys()):
        color = RED
    else:
        color = YELLOW

    draw_station(surface, camera, snapped, "STATION", color=color)

    
    
    