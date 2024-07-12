from dataclasses import dataclass

from voyage_touch import SensorType

@dataclass
class SensorReading:
    sensor_type: SensorType
    sensor_id: int
    value: float
    time: int   # nanoseconds since UNIX epic