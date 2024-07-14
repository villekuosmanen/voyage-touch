# Experiments

Collect touch data with labels to train a ML model for the ASCC, as well as evaluate the trained models.

## Data collection

Manual data collection is simple but can realistically only collect contact data. Data for magnitude of force needs to be collected using an automated system, which also guarantees more data is available.

Current data collection system relies on CSVs. More compressed data formats might be needed to store large future datasets efficiently.

### Downloading datasets

Links to download pre-recorded datasets will be provided in the future.

### Manual

Manual data collection works by pressing the touch points in the tactile sensor using your fingers, while pressing the number keys on the keyboard at the same time.

Try out data collection using this script.

```
python experiments/manual.py
```

### Automated

To be designed.

## Training policies

TO be designed.

## Evaluating models.

You can evaluate the heuristic FSR model using the following script.

The evaluation uses all generated data files inside the `data` folder.

```
python experiments/evaluate_model.py
```
