from pygame import Surface
from config.colors import RED, WHITE
from models.position import Position, PositionWithDirection
from services.bulldoze import CursorTarget, get_bulldoze_target
from ui_elements.draw_utils import draw_node, draw_signal, draw_station, draw_edges
from graphics.camera import Camera
from models.map import RailMap

def render_bulldoze_preview(surface: Surface, world_pos: Position, map: RailMap, camera: Camera):
    target = get_bulldoze_target(map, world_pos, camera.scale)
    
    if target.type == CursorTarget.EMPTY:
        draw_node(surface, camera, target.data, color=RED)
    elif target.type == CursorTarget.STATION:
        draw_station(surface, camera, target.data, map.stations[target.data], color=RED)
    elif target.type == CursorTarget.SIGNAL:
        draw_signal(surface, camera, PositionWithDirection(position=target.data, direction=map.graph.nodes[target.data]['signal']), color=RED)
    elif target.type == CursorTarget.PLATFORM:
        _, edges = map.get_segments_at(target.data)
        draw_edges(surface, edges, camera, color=WHITE)
    elif target.type == CursorTarget.EDGE:
        _, edges = map.get_segments_at(target.data)
        draw_edges(surface, edges, camera, color=RED)
    elif target.type == CursorTarget.NODE:
        nodes, edges = map.get_segments_at(target.data)

        draw_edges(surface, edges, camera, color=RED)
        for node in nodes:
            if map.graph.degree[node] > 2:
                draw_node(surface, camera, node, color=RED)