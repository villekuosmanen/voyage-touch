from dataclasses import dataclass

import numpy as np

@dataclass
class MarkovianDatapoint:
    readings: np.array
    labels: np.array