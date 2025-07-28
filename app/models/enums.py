from enum import Enum

class MovementEvent(str, Enum):
    arrival = "arrival"
    departure = "departure"