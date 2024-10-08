from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass
from typing import List

import numpy as np

from voyage_touch.sensor import SensorReading

@dataclass
class ASSCModelConfig:
    """
    Config for an ASSC model.
    """
    num_points: int
    num_fsr_sensors: int
    num_piezo_sensors: int

class ASSCModel(ABC):
    """
    An abstract class for an ASSC Model. Should be implemented by all ASSC models.
    """

    @abstractmethod
    def get_config(self) -> ASSCModelConfig:
        """
        Retuns the ASSC config of the model. Used by the ASSC class for managing sensor readings.
        """
        pass

    def predict_markovian(self, readings: List[float]) -> np.array:
        """
        Predict touch events (1 or 0) for each point when given the most recent sensor readings.
        """
        pass

    def predict_timeseries(self, readings: List[deque]) -> np.array:
        """
        Predict touch events (1 or 0) for each point when given a time series of sensor readings.
        """
        pass
