# Day 9 - Ocean World Evidence Prediction

This project predicts whether a Solar System ocean-world candidate has
`strong_evidence` or `possible_evidence` for a subsurface ocean.

The dataset is small and included in this folder. It uses ocean-world candidates
such as Europa, Enceladus, Titan, Ganymede, Callisto, Ceres, Pluto, Triton,
Dione, Mimas, Ariel, and Titania.

## Files

- `ocean_world_prediction.py` - loads the data, runs the prediction model, and
  saves a report.
- `data/ocean_worlds.csv` - the included dataset.
- `test_ocean_world_prediction.py` - tests the prediction functions.
- `requirements.txt` - installs pytest for the tests.

## Data

The dataset columns are:

- `world`
- `location`
- `radius_km`
- `density_g_cm3`
- `surface_temp_k`
- `activity_score`
- `ocean_evidence`

`activity_score` is a simple classroom score from 1 to 5. A higher score means
more visible signs of activity, such as plumes, resurfacing, or tidal heating.

The label is:

- `strong_evidence`
- `possible_evidence`

## How To Run

Open a terminal in the `day09` folder.

Install requirements:

```text
python -m pip install -r requirements.txt
```

Run the program:

```text
python ocean_world_prediction.py
```

The program prints a short report and saves it here:

```text
results/prediction_report.txt
```

## How The Prediction Works

The code uses a simple k-nearest neighbors model.

For each test world, it finds the most similar training worlds using:

- radius
- density
- surface temperature
- activity score

The most common label among the nearest worlds becomes the prediction.

## Tests

From the `day09` folder, run:

```text
python -m pytest
```

## Prompt

The assignment was to choose a dataset, create a prediction from the data, add a
README, and make the example easy to rerun.

I changed the topic to astrobiology and used only Solar System ocean-world
candidates instead of planets outside the Solar System.
