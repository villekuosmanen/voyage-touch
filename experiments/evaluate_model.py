from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

import numpy as np
from sklearn.model_selection import train_test_split

from voyage_touch.assc.data import load_markovian_data
from voyage_touch.assc.policies import FSRHeuristicPolicy

NO_OF_FSRS = 3

# Example of how to evaluate an ASSC model

data, labels = load_markovian_data('data') # TODO: load all data
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.8, random_state=42)

policy = FSRHeuristicPolicy(NO_OF_FSRS)
y_pred = np.array([policy.predict_markovian(x) for x in X_test])

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print(f'Accuracy: {accuracy}')
print(f'Precision: {precision}')
print(f'Recall: {recall}')
print(f'F1 Score: {f1}')
