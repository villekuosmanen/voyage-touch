from dataclasses import dataclass
import time

import serial

from voyage_touch.sensor import SensorType

FSR_MAX_READING = 1000
PIEZO_MAX_READING = 160

@dataclass
class SensorReading:
    sensor_type: SensorType
    sensor_id: int
    value: float
    time: int   # nanoseconds since UNIX epic

class TouchSensor:
    """
    Class for communicating via touch sensors. 
    """
    def __init__(self, port, baudrate=115200, timeout=5, num_fsrs=3, num_pzs=3):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.num_fsrs = num_fsrs
        self.num_pzs = num_pzs

        self.should_stop = False

        self.arduino = None

    def connect(self, callback) -> bool:
        self.callback = callback

        # Initialse serial connection
        self.arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1) 
        print("initialising serial connection...")
        time.sleep(0.5)  # Wait for the serial connection to initialize

        for _ in range(100):
            line = self.arduino.readline()
            try:
                line = line.decode('utf-8').strip()
                tokens = line.split(',')
                if len(tokens) != 3:
                    continue
                
                # initialised successfully
                return True
            except:
                continue

        return False
    
    def close(self):
        self.should_stop = True

    def run(self):
        assert self.arduino is not None

        while True:
            if self.should_stop:
                return

            if self.arduino.in_waiting > 0:
                try:
                    line = self.arduino.readline().decode('utf-8').strip()
                except UnicodeDecodeError:
                    continue
                tokens = line.split(',')
                if len(tokens) != 3:
                    print(f"invalid format received via serial: {line}\n")
                    continue
                try:
                    if tokens[0] == "FSR":
                        sensor_id = int(tokens[1])
                        if sensor_id >= self.num_fsrs:
                            # more sensors in the hardware device than our software supports
                            # therefore silently ignore them
                            continue

                        # Convert FSR value to an integer
                        pz_value = int(tokens[2])
                        # Clamp the value between 0 and FSR_MAX_READING
                        pz_value = max(0, min(FSR_MAX_READING, pz_value)) / FSR_MAX_READING
                        
                        # Broadcast
                        reading = SensorReading(SensorType.FSR, sensor_id, pz_value, time.time_ns())
                        self.callback(reading)

                    elif tokens[0] == "PZ":
                        sensor_id = int(tokens[1])
                        if sensor_id >= self.num_pzs:
                            # more sensors in the hardware device than our software supports
                            # therefore silently ignore them
                            continue

                        # Convert FSR value to an integer
                        pz_value = int(tokens[2])
                        # Clamp the value between 0 and PIEZO_MAX_READING
                        pz_value = max(0, min(PIEZO_MAX_READING, pz_value)) / PIEZO_MAX_READING

                        # Broadcast
                        reading = SensorReading(SensorType.PIEZO, sensor_id, pz_value, time.time_ns())
                        self.callback(reading)
                    else:
                        print(f"expected sensor type to be FSR or PZ, got {tokens[0]}\n")
                        continue

                except ValueError:
                    pass  # Ignore invalid values


        

