from dataclasses import dataclass

@dataclass
class ASSCModelConfig:
    """
    Config for an ASSC model.
    """
    num_points: int
    num_fsr_sensors: int
    num_piezo_sensors: int
