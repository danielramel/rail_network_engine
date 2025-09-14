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
        return world_x, world_y
    
    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates"""
        screen_x = (world_x + self.x) * self.scale
        screen_y = (world_y + self.y) * self.scale
        return screen_x, screen_y
    
    def start_drag(self, mouse_x, mouse_y):
        """Start dragging the camera"""
        self.is_dragging = True
        self.drag_start_x = mouse_x
        self.drag_start_y = mouse_y
        self.drag_start_cam_x = self.x
        self.drag_start_cam_y = self.y
    
    def update_drag(self, mouse_x, mouse_y):
        """Update camera position during drag"""
        dx = mouse_x - self.drag_start_x
        dy = mouse_y - self.drag_start_y
        self.x = self.drag_start_cam_x + dx / self.scale
        self.y = self.drag_start_cam_y + dy / self.scale
        
    
    def stop_drag(self):
        """Stop dragging the camera"""
        self.is_dragging = False
    
    def zoom(self, mouse_x, mouse_y, zoom_direction, screen_width, screen_height):
        """Zoom in/out centered on mouse position"""
        zoom_factor = 1.1 if zoom_direction > 0 else 1.0 / 1.1
        
        # Calculate new scale with limits
        new_scale = self.scale * zoom_factor
        if new_scale < self.min_scale:
            zoom_factor = self.min_scale / self.scale
            new_scale = self.min_scale
        elif new_scale > self.max_scale:
            zoom_factor = self.max_scale / self.scale
            new_scale = self.max_scale
        
        if new_scale == self.scale:
            return  # No change needed
        
        # Calculate zoom center relative to current view
        center_x = screen_width / 2
        center_y = screen_height / 2
        
        # Adjust camera position so mouse stays in same world position
        mouse_offset_x = mouse_x - center_x
        mouse_offset_y = mouse_y - center_y
        
        self.x += mouse_offset_x / self.scale * (1 - zoom_factor)
        self.y += mouse_offset_y / self.scale * (1 - zoom_factor)
        
        self.scale = new_scale
    
    def reset(self):
        """Reset camera to default position and scale"""
        self.x = 0.0
        self.y = 0.0
        self.scale = 1.0
    
    def apply_transform(self, surface):
        """Apply camera transform to surface (for drawing)"""
        # This would be used if pygame supported matrix transforms
        # For now we'll transform coordinates manually
        pass
    
    
