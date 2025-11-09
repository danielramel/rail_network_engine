class Time:
    current_time: int = 0  # in seconds
    
    def __init__(self, current_time: int) -> None:
        self.current_time = current_time
    
    def get_hours_minutes_seconds(self) -> tuple[int, int, int]:
        hours = int(self.current_time // 3600)
        minutes = int((self.current_time % 3600) // 60)
        seconds = round(self.current_time % 60)
        return hours, minutes, seconds
    
    def add(self, seconds: float) -> None:
        self.current_time += seconds
        
    def set_time_from_string(self, time_str: str) -> None:
        try:
            parts = time_str.split(":")
            if len(parts) != 3:
                raise ValueError("Time must be in HH:MM:SS format")
            hours, minutes, seconds = map(int, parts)
            self.current_time = hours * 3600 + minutes * 60 + seconds
        except Exception as e:
            print(f"Invalid time format: {e}")