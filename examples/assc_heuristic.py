

from voyage_touch.sensor import SensorType, TouchSensor, TouchSensorReader

# Example for using an ASSC with a heuristic model.

if __name__ == '__main__':
    sensor = TouchSensor('/dev/ttyACM0')
