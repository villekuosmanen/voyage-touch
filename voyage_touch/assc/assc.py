import asyncio
from threading import Thread

import numpy as np

from voyage_touch.assc import ASSCModelConfig
from voyage_touch.sensor import SensorReading, TouchSensor

class ASSC:
    """
    Artificial somatosensory cortex.

    Predicts tactile events based on sensor data.
    """
    def __init__(self, config: ASSCModelConfig, sensor: TouchSensor, sensor_reading_time_window=5000):
        self.sensor = sensor

        assert sensor.num_fsrs == config.num_fsr_sensors
        assert sensor.num_pzs == config.num_piezo_sensors
        
        self.num_points = config.num_points
        self.num_fsr_sensors = config.num_fsr_sensors
        self.num_piezo_sensors = config.num_piezo_sensors

        # maintain a time window of sensor readings
        # TODO
    
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
        # TODO
        pass

    def predict() -> np.array:
        """
        For every point in the ASSC model, predict the current touch event state.
        """
        # TODO
        pass
