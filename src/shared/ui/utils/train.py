import pygame

from core.graphics.camera import Camera
from core.models.geometry.edge import Edge

from .tracks import draw_occupied_edge

def draw_train(surface: pygame.Surface, edges: tuple[Edge], camera: Camera, color: tuple[int, int, int], edge_progress: float = 0.0) -> None:
    draw_occupied_edge(surface, edges[0].a, edges[0].b, camera, color=color, edge_progress=edge_progress, is_last=True)
    for edge in edges[1:-1]:
        draw_occupied_edge(surface, edge.a, edge.b, camera, color=color, edge_progress=edge_progress)
    draw_occupied_edge(surface, edges[-1].a, edges[-1].b, camera, color=color, edge_progress=edge_progress, is_first=True)