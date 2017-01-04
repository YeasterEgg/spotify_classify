import numpy as np
import pandas as pd

def run_perceptron(X, Y, bias, max_iter):
  n_samples, n_variables = len(X), len(X[0])
  weights = [0] * n_variables
  errors = []
  for i in range(max_iter):
    current_errors = 0
    for j in range(n_samples):
      sample_values = X[j]
      result = Y[j]
      predicted = bias + array_dot(weights, sample_values)
      if(result * predicted <= 0):
        weights += result * sample_values
        bias += result
        current_errors += 1
    errors.append(current_errors)
  print(errors)
  return weights

def array_dot(x, y):
  return sum([i*j for (i, j) in zip(x, y)])

def store_weights(mysql, moods, X, Y, bias = 0, max_iter = 100):
  moods_tuple = tuple(sorted(moods))
  mood_couple = "_".join(mood for mood in moods_tuple)
  df = read_database(mysql, moods_tuple)
  X = df.drop("mood",1)
  Y = pd.get_dummies(df[["mood"]])
  run_perceptron(X, Y, bias, max_iter)

def read_database(mysql, moods_tuple, threshold = 1):
  return pd.read_sql_query("SELECT spotify_id, mood, duration_ms, danceability, acousticness, energy, liveness, valence, instrumentalness, tempo, speechiness, loudness FROM tracks WHERE mood in {} AND count > {}".format(moods_tuple, threshold), con = mysql, index_col = ["spotify_id"])
