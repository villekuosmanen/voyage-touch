import asyncio
from collections import deque
import time
from threading import Thread

import numpy as np

from voyage_touch.assc import ASSCModel
from voyage_touch.sensor import SensorType, SensorReading, TouchSensor

class ASSC:
    """
    Artificial somatosensory cortex.

    Predicts tactile events based on sensor data.
    """
    def __init__(self, model: ASSCModel, sensor: TouchSensor, sensor_reading_time_window=5000):
        """
        sensor_reading_time_window: time window in milliseconds.
        """
        self.sensor = sensor
        self.model = model
        config = model.get_config()

        assert sensor.num_fsrs == config.num_fsr_sensors
        assert sensor.num_pzs == config.num_piezo_sensors
        
        self.time_window = sensor_reading_time_window * 1_000_000   # convert to nanoseconds
        self.num_points = config.num_points
        self.num_fsr_sensors = config.num_fsr_sensors
        self.num_piezo_sensors = config.num_piezo_sensors

        # maintain a time window of sensor readings for each sensor
        self.readings = [deque()]*(sensor.num_fsrs + sensor.num_pzs)
    
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

        current_time = time.time_ns()
        self.readings[sensor_id].append((current_time, reading))
        self._remove_old_readings(sensor_id, current_time)

    def _remove_old_readings(self, sensor_id, current_time):
        while self.readings[sensor_id] and (current_time - self.readings[sensor_id][0][0]) > self.time_window:
            self.readings[sensor_id].popleft()


    def predict(self) -> np.array:
        """
        For every point in the ASSC model, predict the current touch event state.
        """
        return self.model.predict(self.readings)
