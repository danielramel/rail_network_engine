from models.geometry import Point


class Camera:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.scale = 1.0
        self.min_scale = 0.4
        self.max_scale = 8.0
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.drag_start_cam_x = 0
        self.drag_start_cam_y = 0
        
    def screen_to_world(self, screen_x, screen_y):
        """Convert screen coordinates to world coordinates"""
        world_x = (screen_x / self.scale) - self.x
        world_y = (screen_y / self.scale) - self.y
        return Point(world_x, world_y)
    
    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates"""
        screen_x = (world_x + self.x) * self.scale
        screen_y = (world_y + self.y) * self.scale
        return Point(screen_x, screen_y)
    
    def start_drag(self, mouse_x, mouse_y):
        """Start dragging the camera"""
        self.is_dragging = True
        self.drag_start_x = mouse_x
        self.drag_start_y = mouse_y
        self.drag_start_cam_x = self.x
        self.drag_start_cam_y = self.y
    
    def update_drag(self, mouse_x, mouse_y):
        """Update camera position during drag"""
        if not self.is_dragging:
            return
        dx = mouse_x - self.drag_start_x
        dy = mouse_y - self.drag_start_y
        self.x = self.drag_start_cam_x + dx / self.scale
        self.y = self.drag_start_cam_y + dy / self.scale
        
    
    def stop_drag(self):
        """Stop dragging the camera"""
        self.is_dragging = False
    
    def zoom(self, mouse_pos: Point, zoom_direction):
        """Zoom in/out centered on mouse position"""

        zoom_factor = 1.1 if zoom_direction > 0 else 1.0 / 1.1
        new_scale = self.scale * zoom_factor
        new_scale = max(self.min_scale, min(new_scale, self.max_scale))
        
        if new_scale == self.scale:
            return  # No change needed

        world_x, world_y = self.screen_to_world(mouse_pos.x, mouse_pos.y)

        self.scale = new_scale

        # Calculate where that world position would appear on screen with new scale
        new_screen_x, new_screen_y = self.world_to_screen(world_x, world_y)
        
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

    def is_click(self, pos):
        x, y = pos
        return self.is_dragging and x == self.drag_start_x and y == self.drag_start_y
    
    
