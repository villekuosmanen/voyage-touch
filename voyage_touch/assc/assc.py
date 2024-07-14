from abc import ABC, abstractmethod
from threading import Thread

import numpy as np

class ASSC(ABC):
    """
    Artificial somatosensory cortex.

    Predicts tactile events based on sensor data.
    """

    @abstractmethod    
    async def start(self) -> Thread:
        """
        Starts the ASSC in a separate thread.
        """
        pass
    
    @abstractmethod
    def stop(self):
        """
        Stops the currently running ASSC.
        """
        pass

    @abstractmethod
    def predict(self) -> np.array:
        """
        For every point in the ASSC model, predict the current touch event state.
        """
        pass
