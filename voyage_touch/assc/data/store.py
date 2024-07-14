import csv
from dataclasses import dataclass
import os
from typing import List

import numpy as np

from voyage_touch.assc.data import MarkovianDatapoint

def _get_next_filename(directory: str, prefix: str, extension: str, digits: int = 4) -> str:
    existing_files = os.listdir(directory)
    max_num = 0
    for filename in existing_files:
        if filename.startswith(prefix) and filename.endswith(extension):
            num_str = filename[len(prefix):-len(extension)]
            if num_str.isdigit():
                num = int(num_str)
                if num > max_num:
                    max_num = num
    next_num = max_num + 1
    next_filename = f"{prefix}{next_num:0{digits}}{extension}"
    return os.path.join(directory, next_filename)


def store_markovian_data(
    directory: str,
    data: List[MarkovianDatapoint],
    prefix: str = "experiment",
    extension: str = ".csv",
):
    """
    Store in CSV format.
    """
    filepath = _get_next_filename(directory, prefix, extension)
    
    with open(filepath, 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['readings', 'labels'])  # Write header
        for datapoint in data:
            readings_str = ','.join(map(str, datapoint.readings))
            labels_str = ','.join(map(str, datapoint.labels))
            writer.writerow([readings_str, labels_str])
