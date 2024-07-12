import asyncio
from queue import Queue
import time
from threading import Thread, Lock
from typing import Optional

import serial

from voyage_touch import SensorType
from voyage_touch import SensorReading

FSR_MAX_READING = 1000
PIEZO_MAX_READING = 160

class TouchSensor:
    def __init__(self, port, baudrate=115200, timeout=5, num_fsrs=3, num_pzs=3):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.num_fsrs = num_fsrs
        self.num_pzs = num_pzs

        self.should_stop = False
        self.queues = {}
        self.mutex = Lock()

        self.sensor_readings = [None]*(num_fsrs + num_pzs)

    
    def register_listener(self, listener_id: int, q: Queue):
        """
        Registers a new listener queue. All sensor data will be written here.
        """
        with self.mutex:
            self.queues[listener_id] = q

    def deregister_listener(self, listener_id: int):
        """
        Deregisters a listener queue. No more data will be written to the queue.
        """
        with self.mutex:
            self.queues.pop(listener_id, None)

    async def start(self) -> Thread:
        # Initialse serial connection
        arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1) 
        print("initialising serial connection...")
        time.sleep(0.5)  # Wait for the serial connection to initialize

        success = False
        for i in range(100):
            line = arduino.readline()
            try:
                line = line.decode('utf-8').strip()
                tokens = line.split(',')
                if len(tokens) != 3:
                    continue
                
                # initialised successfully
                success = True
                break
            except:
                continue

        if not success:
            print(f"failed to initialise serial connection")
            return

        sensor_thread = Thread(target=lambda: asyncio.run(self._run(arduino)))
        
        print("serial connection initialised!")

        sensor_thread.start()
        return sensor_thread
    
    def stop(self):
        self.should_stop = True

    def read(self, sensor_type: SensorType, sensor_id: int) -> Optional[SensorReading]:
        """
        Returns the current sensor reading for the current sensor ID.
        """
        if sensor_type is SensorType.PIEZO:
            sensor_id += self.num_fsrs

        if sensor_id >= len(self.sensor_readings) or sensor_id < 0:
            raise ValueError("sensor id outside expected range - no such sensor exists")
        
        return self.sensor_readings[sensor_id]

    async def _run(self, arduino):
        """
        Starts the sensor reader in a separate thread. Blocks until the connection cuts off or the sensor is stopped.
        """
        while True:
            if self.should_stop:
                return

            if arduino.in_waiting > 0:
                try:
                    line = arduino.readline().decode('utf-8').strip()
                except UnicodeDecodeError:
                    continue
                tokens = line.split(',')
                if len(tokens) != 3:
                    print(f"invalid format received via serial: {line}\n")
                    continue
                try:
                    if tokens[0] == "FSR":
                        sensor_id = int(tokens[1])

                        # Convert FSR value to an integer
                        pz_value = int(tokens[2])
                        # Clamp the value between 0 and FSR_MAX_READING
                        pz_value = max(0, min(FSR_MAX_READING, pz_value)) / FSR_MAX_READING
                        
                        # Broadcast
                        reading = SensorReading(SensorType.FSR, sensor_id, pz_value, time.time_ns())
                        with self.mutex:
                            for q in self.queues.values():
                                q.put(reading)
                        self.sensor_readings[sensor_id] = reading

                    elif tokens[0] == "PZ":
                        sensor_id = int(tokens[1])

                        # Convert FSR value to an integer
                        pz_value = int(tokens[2])
                        # Clamp the value between 0 and PIEZO_MAX_READING
                        pz_value = max(0, min(PIEZO_MAX_READING, pz_value)) / PIEZO_MAX_READING

                        # Broadcast
                        reading = SensorReading(SensorType.PIEZO, sensor_id, pz_value, time.time_ns())
                        with self.mutex:
                            for q in self.queues.values():
                                q.put(reading)
                        self.sensor_readings[sensor_id + self.num_fsrs] = reading
                    else:
                        print(f"expected sensor type to be FSR or PZ, got {tokens[0]}\n")
                        continue

                except ValueError:
                    pass  # Ignore invalid values
