import csv
import os

import numpy as np

def load_markovian_data(directory: str):
    all_data = []
    all_labels = []

    for filename in os.listdir(directory):
        if filename.startswith('experiment') and filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    readings = np.array(list(map(float, row['readings'].split(','))))
                    label = np.array(list(map(float, row['labels'].split(','))))
                    all_data.append(readings)
                    all_labels.append(label)
    
    return np.array(all_data), np.array(all_labels)

