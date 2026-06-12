# Day 9 - Exoplanet Temperateness Prediction

This project uses confirmed exoplanet data from the NASA Exoplanet Archive. The
goal is to predict whether an exoplanet is `temperate` or `not_temperate` from
planet and star measurements.

This relates to astrobiology because temperate planets are more interesting when
thinking about possible habitability. This program is not claiming that a planet
is habitable. It only makes a simple prediction based on equilibrium
temperature.

The prediction program uses a small k-nearest neighbors model written in regular
Python. It does not need pandas, scikit-learn, or any other machine-learning
package.

## Dataset

Dataset: Planetary Systems Composite Parameters

Source: NASA Exoplanet Archive

NASA TAP documentation:

```text
https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html
```

NASA column documentation:

```text
https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html
```

The program downloads a CSV from the NASA Exoplanet Archive TAP service. It uses
this table:

```text
pscomppars
```

It downloads these columns:

- `pl_name` - planet name
- `hostname` - host star name
- `pl_orbper` - orbital period
- `pl_rade` - planet radius
- `st_teff` - stellar effective temperature
- `st_rad` - stellar radius
- `st_mass` - stellar mass
- `pl_eqt` - planet equilibrium temperature

The prediction uses the planet/star measurements as inputs. It uses
`pl_eqt` only to create the answer label:

- `temperate` if equilibrium temperature is between 180 K and 310 K
- `not_temperate` otherwise

## Files

- `exoplanet_prediction.py` - downloads the dataset, trains the prediction
  model, and prints/saves the results.
- `test_exoplanet_prediction.py` - tests the prediction functions without using
  the internet.
- `requirements.txt` - installs pytest for the optional tests.
- `README.md` - this file.

When the script runs, it creates:

- `data/exoplanets.csv` - the downloaded dataset.
- `results/prediction_report.txt` - the prediction summary.

## How To Download The Data

The easiest way is to run the program. If `data/exoplanets.csv` is missing, the
script downloads it automatically:

```text
python exoplanet_prediction.py
```

If you want to download it manually, open this URL in a browser:

```text
https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,hostname,pl_orbper,pl_rade,st_teff,st_rad,st_mass,pl_eqt+from+pscomppars+where+pl_orbper+is+not+null+and+pl_rade+is+not+null+and+st_teff+is+not+null+and+st_rad+is+not+null+and+st_mass+is+not+null+and+pl_eqt+is+not+null&format=csv
```

Save the file as:

```text
day09/data/exoplanets.csv
```

Then run:

```text
python exoplanet_prediction.py
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
python exoplanet_prediction.py
```

The program prints the accuracy and the first 10 predictions. It also saves the
same report in:

```text
results/prediction_report.txt
```

## What The Prediction Does

The script splits the data into:

- training rows
- testing rows

For each test planet, it finds the closest training planets using:

- orbital period
- planet radius
- stellar effective temperature
- stellar radius
- stellar mass

The most common label among the closest planets becomes the prediction.

This method is called k-nearest neighbors.

## How To Run The Tests

From the `day09` folder, run:

```text
python -m pytest
```

The tests use small fake data, so they do not need the internet.

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
