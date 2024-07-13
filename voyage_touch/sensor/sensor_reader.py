import asyncio
from queue import Queue
from threading import Thread, Lock
from typing import Optional

from voyage_touch.sensor import SensorReading, SensorType, TouchSensor

FSR_MAX_READING = 1000
PIEZO_MAX_READING = 160

class TouchSensorReader:
    """
    A convenient class for reading raw data from touch sensors via serial connections.
    """
    def __init__(self, sensor: TouchSensor):
        self.sensor = sensor
        self.queues = {}
        self.mutex = Lock()

        self.sensor_readings = [None]*(sensor.num_fsrs + sensor.num_pzs)

    
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
        success = self.sensor.connect(self.sensor_callback)
        if not success:
            raise ValueError("failed to connect via serial")
        
        print("serial connection initialised!")
        
        sensor_thread = Thread(target=lambda: asyncio.run(self.sensor.run()))
        sensor_thread.start()
        return sensor_thread
    
    def stop(self):
        self.sensor.close()
    
    def sensor_callback(self, reading: SensorReading):
        sensor_id = reading.sensor_id
        if reading.sensor_type is SensorType.PIEZO:
            sensor_id += self.sensor.num_fsrs

        with self.mutex:
            for q in self.queues.values():
                q.put(reading)
        self.sensor_readings[sensor_id] = reading

    def read(self, sensor_type: SensorType, sensor_id: int) -> Optional[SensorReading]:
        """
        Returns the current sensor reading for the current sensor ID.
        """
        if sensor_type is SensorType.PIEZO:
            sensor_id += self.sensor.num_fsrs

        if sensor_id >= len(self.sensor_readings) or sensor_id < 0:
            raise ValueError("sensor id outside expected range - no such sensor exists")
        
        return self.sensor_readings[sensor_id]
