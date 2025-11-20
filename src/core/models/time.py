from math import floor

class Time:
    current_time: float = None  # in seconds
        
    def get_hms(self) -> tuple[str, str, str]:
        if self.current_time is None:
            return "--", "--", "--"
        hours = str(int(self.current_time // 3600))
        minutes = str(int((self.current_time % 3600) // 60))
        seconds = str(floor(self.current_time % 60))
        return hours, minutes, seconds
    
    def add(self, seconds: float) -> None:
        self.current_time += seconds
        self.current_time %= 24 * 3600  # wrap around after 24 hours
        
    def set_time_from_string(self, time_str: str) -> None:
        try:
            parts = time_str.split(":")
            if len(parts) != 3:
                raise ValueError("Time must be in HH:MM:SS format")
            hours, minutes, seconds = map(int, parts)
            self.current_time = hours * 3600 + minutes * 60 + seconds
        except ValueError as e:
            pass
            #TODO it bugs out
            #TODO handle this differently