class Color:
    WHITE = (255, 255, 255)
    GREY = (180, 180, 180)
    GREEN = (0, 200, 0)
    BLACK = (0, 0, 0)
    RED = (200, 0, 0)
    YELLOW = (200, 200, 0)
    PURPLE = (128, 0, 128)
    CYAN = (0, 200, 200)
    MAGENTA = (200, 0, 200)
    ORANGE = (255, 165, 0)
    BROWN = (165, 42, 42)
    LIGHTBLUE = (173, 216, 230)
    BLUE = (0, 0, 255)
    LIME = (0, 255, 0)
    DARKGREY = (100, 100, 100)
    LIGHTGREY = (200, 200, 200)
    PINK = (255, 192, 203)
    
    def get(color_name: str) -> tuple[int, int, int]:
        return getattr(Color, color_name.upper(), Color.WHITE)
    
    def all() -> list[str]:
        return [attr for attr in dir(Color) if not attr.startswith("__") and attr.isupper()]