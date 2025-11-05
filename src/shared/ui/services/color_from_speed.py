        
def color_from_speed(speed: int) -> tuple[int, int, int]:
    # Clamp to valid range
    speed = max(0, min(speed, 200))

    # Define color stops (speed, (R,G,B))
    gradient = [
        (10,  (0, 0, 255)),     # Blue
        (80,  (0, 255, 255)),   # Cyan
        (120, (0, 255, 0)),     # Green
        (150, (255, 255, 0)),   # Yellow
        (200,   (128, 0, 128)),   # Purple
    ]

    # Find which two stops we’re between
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