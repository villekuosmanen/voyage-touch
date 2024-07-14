
from collections import deque
from typing import List

import numpy as np

from voyage_touch.sensor import SensorReading
from voyage_touch.assc import ASSCModel, ASSCModelConfig

class FSRHeuristicPolicy(ASSCModel):
    """
    A heuristic policy for sensors that only contain force sensing resistors.
    Each force sensing resistor is a sensor point.
    Predicts touch events, where voltage > 0 is considered true. 
    """
    def __init__(self, num_fsrs: int, floor = 0.02):
        self.config = ASSCModelConfig(
            num_points=num_fsrs,
            num_fsr_sensors=num_fsrs,
            num_piezo_sensors=0,
        )
        self.floor = floor
    
    def get_config(self) -> ASSCModelConfig:
        return self.config
    
    def predict_markovian(self, readings: List[SensorReading]) -> np.array:
        res = np.zeros(self.config.num_points)
        for i, reading in enumerate(readings):
            if reading is not None and reading.value > self.floor:
                res[i] = 1
        return res
    
    def predict_timeseries(self, readings: List[deque]) -> np.array:
        raise NotImplementedError("FSRHeuristicPolicy only supports Markovian ASSCs.")
