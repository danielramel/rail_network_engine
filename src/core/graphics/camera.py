from models.geometry import Position
from models.geometry.edge import Edge

class Camera:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.scale = 1.0
        self.min_scale = 0.1
        self.max_scale = 3.0
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.drag_start_cam_x = 0
        self.drag_start_cam_y = 0

    def screen_to_world(self, pos: Position | Edge) -> Position | Edge:
        """Convert screen coordinates to world coordinates"""
        if isinstance(pos, Edge):
            return Edge(self.screen_to_world(pos.a), self.screen_to_world(pos.b))

        world_x = (pos.x / self.scale) - self.x
        world_y = (pos.y / self.scale) - self.y
        return Position(world_x, world_y)

    def world_to_screen(self, obj: Position | Edge) -> Position | Edge:
        """Convert world coordinates to screen coordinates"""
        if isinstance(obj, Edge):
            return Edge(self.world_to_screen(obj.a), self.world_to_screen(obj.b))

        screen_x = (obj.x + self.x) * self.scale
        screen_y = (obj.y + self.y) * self.scale
        return Position(screen_x, screen_y)

    
    def start_drag(self, mouse_pos: Position):
        """Start dragging the camera"""
        self.is_dragging = True
        self.drag_start_x = mouse_pos.x
        self.drag_start_y = mouse_pos.y
        self.drag_start_cam_x = self.x
        self.drag_start_cam_y = self.y

    def update_drag(self, mouse_pos : Position):
        """Update camera position during drag"""
        if not self.is_dragging:
            return
        dx = mouse_pos.x - self.drag_start_x
        dy = mouse_pos.y - self.drag_start_y
        self.x = self.drag_start_cam_x + dx / self.scale
        self.y = self.drag_start_cam_y + dy / self.scale
        
    
    def stop_drag(self, pos: Position):
        """Stop dragging the camera"""
        was_dragging = self.is_dragging
        self.is_dragging = False
        buffer = 5  # pixels tolerance to avoid tiny accidental drags
        dx = pos.x - self.drag_start_x
        dy = pos.y - self.drag_start_y
        return was_dragging and (abs(dx) > buffer or abs(dy) > buffer)

    def zoom(self, mouse_pos: Position, zoom_direction: int):
        """Zoom in/out centered on mouse position"""

        zoom_factor = 1.2 if zoom_direction > 0 else 1.0 / 1.2
        # compute new scale and round to nearest 5% increment (0.05)
        new_scale = round(self.scale * zoom_factor / 0.05) * 0.05
        new_scale = max(self.min_scale, min(new_scale, self.max_scale))
        
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
        self.x = 0.0
        self.y = 0.0
        self.scale = 1.0
        
    def is_reset(self) -> bool:
        return self.x == 0.0 and self.y == 0.0 and self.scale == 1.0