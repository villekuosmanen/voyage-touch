import asyncio
from collections import deque
import time
from threading import Thread

import numpy as np

from voyage_touch.assc import ASSCModel, ASSC
from voyage_touch.sensor import SensorType, SensorReading, TouchSensor

class MarkovianASSC(ASSC):
    """
    Markovian Artificial somatosensory cortex.

    Predicts tactile events based on sensor data. Only considers the most recent measurements when making a prediction
    """
    def __init__(self, model: ASSCModel, sensor: TouchSensor):
        """
        sensor_reading_time_window: time window in milliseconds.
        """
        self.sensor = sensor
        self.model = model
        config = model.get_config()

        assert sensor.num_fsrs == config.num_fsr_sensors
        assert sensor.num_pzs == config.num_piezo_sensors
        
        self.num_points = config.num_points
        self.num_fsr_sensors = config.num_fsr_sensors
        self.num_piezo_sensors = config.num_piezo_sensors

        # maintain most recent readings for each sensor
        self.readings = [None]*(sensor.num_fsrs + sensor.num_pzs)
    
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
            
        self.readings[sensor_id] = reading

    def predict(self) -> np.array:
        """
        For every point in the ASSC model, predict the current touch event state.
        """
        return self.model.predict_markovian(self.readings)