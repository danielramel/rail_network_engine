from core.config.color import Color    
def color_from_speed(speed: int) -> tuple[int, int, int]:
    # Clamp to valid range
    speed = max(0, min(speed, 200))

    gradient = [
        (10,  Color.BLUE),
        (80,  Color.CYAN),
        (120, Color.ORANGE),
        (150, Color.YELLOW),
        (200,   Color.PINK),
    ]

    for i in range(len(gradient) - 1):
        s0, c0 = gradient[i]
        s1, c1 = gradient[i + 1]
        if s0 <= speed <= s1:
            ratio = (speed - s0) / (s1 - s0)
            r = int(c0[0] + (c1[0] - c0[0]) * ratio)
            g = int(c0[1] + (c1[1] - c0[1]) * ratio)
            b = int(c0[2] + (c1[2] - c0[2]) * ratio)
            return (r, g, b)

    return gradient[-1][1]  # fallback