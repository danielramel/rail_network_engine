from core.config.settings import Config
from core.models.geometry.node import Node
from core.models.geometry.position import Position
from core.models.geometry.edge import Edge

class Camera:
    MIN_SCALE = 0.4
    MAX_SCALE = 3.0
    drag_start_x = 0
    drag_start_y = 0
    drag_start_cam_x = 0
    drag_start_cam_y = 0
    def __init__(self, middle_position: Position, screen_width: int, screen_height: int):
        self.scale = self.MIN_SCALE
        
        self.reset_x = screen_width / (2 * self.scale) - middle_position.x * Config.GRID_SIZE
        self.reset_y = screen_height / (2 * self.scale) - middle_position.y * Config.GRID_SIZE
        self.x = self.reset_x
        self.y = self.reset_y

        
    def factor(self, value: float) -> float:
        """Scale a value according to the current camera scale"""
        return value * self.scale

    def screen_to_world(self, pos: Position | Edge) -> Position | Edge:
        """Convert screen coordinates to world coordinates"""
        if isinstance(pos, Edge):
            return Edge(self.screen_to_world(pos.a), self.screen_to_world(pos.b))

        world_x = ((pos.x / self.scale) - self.x) / Config.GRID_SIZE
        world_y = ((pos.y / self.scale) - self.y) / Config.GRID_SIZE
        return Position(world_x, world_y)

    def world_to_screen(self, pos: Position | Node | Edge) -> Position | Edge:
        """Convert world coordinates to screen coordinates"""
        if isinstance(pos, Edge):
            return Edge(self.world_to_screen(pos.a), self.world_to_screen(pos.b))

        screen_x = (pos.x * Config.GRID_SIZE + self.x) * self.scale
        screen_y = (pos.y * Config.GRID_SIZE + self.y) * self.scale
        return Position(screen_x, screen_y)

    
    def start_drag(self, mouse_pos: Position):
        """Start dragging the camera"""
        self.drag_start_x = mouse_pos.x
        self.drag_start_y = mouse_pos.y
        self.drag_start_cam_x = self.x
        self.drag_start_cam_y = self.y

    def update_drag(self, mouse_pos : Position):
        """Update camera position during drag"""
        dx = mouse_pos.x - self.drag_start_x
        dy = mouse_pos.y - self.drag_start_y
        self.x = self.drag_start_cam_x + dx / self.scale
        self.y = self.drag_start_cam_y + dy / self.scale
        
    
    def stop_drag(self, pos: Position):
        """Stop dragging the camera"""
        buffer = 5  # pixels tolerance to avoid tiny accidental drags
        return pos.distance_to(Position(self.drag_start_x, self.drag_start_y)) < buffer

    def zoom(self, mouse_pos: Position, zoom_direction: int):
        """Zoom in/out centered on mouse position"""

        zoom_factor = 1.2 if zoom_direction > 0 else 1.0 / 1.2
        # compute new scale and round to nearest 5% increment (0.05)
        new_scale = round(self.scale * zoom_factor / 0.05) * 0.05
        new_scale = max(self.MIN_SCALE, min(new_scale, self.MAX_SCALE))
        
        if new_scale == self.scale:
            return  # No change needed

        world_pos = self.screen_to_world(mouse_pos)

        self.scale = new_scale

        # Calculate where that world position would appear on screen with new scale
        new_screen_x, new_screen_y = self.world_to_screen(world_pos)
        
        # Adjust camera to keep world point under mouse
        screen_dx = new_screen_x - mouse_pos.x
        screen_dy = new_screen_y - mouse_pos.y

        self.x -= screen_dx / self.scale
        self.y -= screen_dy / self.scale
    
    def reset(self):
        """Reset camera to default position and scale"""
        self.x = self.reset_x
        self.y = self.reset_y
        self.scale = self.MIN_SCALE
        
    def is_reset(self) -> bool:
        return self.x == self.reset_x and self.y == self.reset_y and self.scale == self.MIN_SCALE