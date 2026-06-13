# Day 9 - Kepler Exoplanet Signal Prediction

This project uses real data from the NASA Exoplanet Archive to predict whether a
Kepler Object of Interest is a confirmed exoplanet or a false positive.

This is similar to the classic Iris machine-learning example:

- Iris uses flower measurements to predict the flower species.
- This project uses Kepler transit and star measurements to predict the KOI
  disposition.

The machine-learning code uses scikit-learn:

```python
model.fit(training_inputs, training_answers)
predictions = model.predict(test_inputs)
```

## Dataset

Dataset: Kepler Objects of Interest, cumulative table

Source: NASA Exoplanet Archive

NASA TAP documentation:

```text
https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html
```

NASA column documentation:

```text
https://exoplanetarchive.ipac.caltech.edu/docs/API_kepcandidate_columns.html
```

The program downloads a CSV from the NASA Exoplanet Archive TAP service. It uses
this table:

```text
cumulative
```

It downloads only rows where `koi_disposition` is either:

- `CONFIRMED`
- `FALSE POSITIVE`

Rows labelled `CANDIDATE` are left out because they are not final labels.

## Prediction

The program gives the model these input measurements:

- `koi_period` - orbital period
- `koi_duration` - transit duration
- `koi_depth` - how much the star dims during the transit
- `koi_impact` - transit geometry
- `koi_prad` - estimated planet radius
- `koi_steff` - star temperature
- `koi_srad` - star radius
- `koi_slogg` - star surface gravity
- `koi_kepmag` - Kepler-band brightness

The model predicts this answer:

```text
koi_disposition
```

The answer is either:

- `CONFIRMED`
- `FALSE POSITIVE`

## Files

- `kepler_koi_prediction.py` - downloads the dataset, trains the model, and
  saves a report.
- `test_kepler_koi_prediction.py` - tests the program with a small fake CSV, so
  tests do not need the internet.
- `requirements.txt` - installs pytest and scikit-learn.
- `README.md` - this file.

When the script runs, it creates:

- `data/kepler_koi.csv` - the downloaded NASA dataset.
- `results/prediction_report.txt` - the prediction summary.

## How To Download The Data

The easiest way is to run the program. If `data/kepler_koi.csv` is missing, the
script downloads it automatically:

```text
python kepler_koi_prediction.py
```

If you want to download it manually, open this URL in a browser:

```text
https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+kepoi_name,koi_disposition,koi_period,koi_duration,koi_depth,koi_impact,koi_prad,koi_steff,koi_srad,koi_slogg,koi_kepmag+from+cumulative+where+koi_disposition+in+('CONFIRMED','FALSE+POSITIVE')+and+koi_period+is+not+null+and+koi_duration+is+not+null+and+koi_depth+is+not+null+and+koi_impact+is+not+null+and+koi_prad+is+not+null+and+koi_steff+is+not+null+and+koi_srad+is+not+null+and+koi_slogg+is+not+null+and+koi_kepmag+is+not+null&format=csv
```

Save the file as:

```text
day09/data/kepler_koi.csv
```

Then run:

```text
python kepler_koi_prediction.py
```

## How To Run

Open a terminal in the `day09` folder:

```text
cd day09
```

Install requirements:

```text
python -m pip install -r requirements.txt
```

Run the prediction:

```text
python kepler_koi_prediction.py
```

The program prints the accuracy and the first 10 predictions. It also saves the
same report in:

```text
results/prediction_report.txt
```

## How The Machine Learning Works

The script splits the NASA rows into:

- training rows
- testing rows

The model learns from the training rows. Each training row has input
measurements and the known answer from NASA:

```text
inputs -> CONFIRMED or FALSE POSITIVE
```

After training, the model receives test rows without looking at their answers.
It predicts the label, and the program compares the prediction to the real NASA
label to calculate accuracy.

The model is a k-nearest neighbors classifier. It predicts a test object by
looking for the most similar objects in the training data and copying the most
common label among those neighbors.

## Tests

From the `day09` folder, run:

```text
python -m pytest
```

The tests use a small fake CSV, so they do not need the internet.

## Prompts

### Prompt 1

for day09 i was assigned - Pick a dataset that you would like to analyze. You
can use one from your lab. You can ask ChatGPT to recommend one. You could
download one from Kaggle or from any other place you find and like.

Create a prediction base on the data.

Add a README and make it easy for us to rerun the example providing clear
instruction how to download the data. Include your prompts.

### Prompt 2

i do not want iris prediction for day 9 also in the code explanation and the
whole programs from day 8 you wrote that you are using path in case there is a
compound txt file but there is none so why do this?

### Prompt 3

no i dont want a wine list. i want a dataset that relates to astrobiology please

### Prompt 4

I want this to be closer to the machine-learning examples where the model learns
from sample inputs and predicts a class, like Iris flower prediction or
cat-versus-dog prediction.
