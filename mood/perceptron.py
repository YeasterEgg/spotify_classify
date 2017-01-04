import random
import pandas as pd
import pdb

def run_perceptron(X, Y, bias, sigma, max_iter, accuracy_limit):
  n_samples, n_variables = len(X), len(X[0])
  weights = [0] * n_variables
  accuracy = 0
  samples = list(zip(X, Y))
  random.shuffle(samples)
  for i in range(max_iter):
    if accuracy >= accuracy_limit:
      print("Reached accuracy limit after {} iterations!".format(i))
      break
    errors = 0
    for sample, result in samples:
      if array_dot(weights, sample) + bias > 0:
        predicted = +1
      else:
        predicted = -1
      if predicted != result:
        new_delta = sigma * result
        weights = [x + y * new_delta for x, y in zip(weights, sample)]
        bias += new_delta
        errors += 1
    print(errors)
    accuracy = (n_samples - errors) / n_samples
    print("Iteration: {} - accuracy: {}".format(i, accuracy))
  return weights, accuracy, bias

def array_dot(x, y):
  return sum([i*j for (i, j) in zip(x, y)])

def read_songs(mysql, moods):
  moods_tuple = tuple(sorted(moods))
  mood_couple = "_".join(mood for mood in moods_tuple)
  df = read_database(mysql, moods_tuple)
  X = df.drop("mood",1).as_matrix()
  dictionary = {"happy": +1, "sad": -1}
  Y = list(dictionary[i[0]] for i in df[["mood"]].as_matrix())
  return X, Y, mood_couple

def get_weights(mysql, moods, bias = 0, sigma = 0.01, max_iter = 1000, accuracy_limit = 0.95):
  X, Y, mood_couple = read_songs(mysql, moods)
  weights, accuracy, bias = run_perceptron(X, Y, bias, sigma, max_iter, accuracy_limit)
  write_weights(mysql, mood_couple, accuracy, bias, weights)

def read_database(mysql, moods_tuple, threshold = 1):
  return pd.read_sql_query("SELECT spotify_id, mood, duration_ms, danceability, acousticness, energy, liveness, valence, instrumentalness, tempo, speechiness, loudness FROM tracks WHERE mood in {} AND count > {}".format(moods_tuple, threshold), con = mysql, index_col = ["spotify_id"])

def write_weights(mysql, mood_couple, accuracy, bias, weights):
  data = tuple([mood_couple, accuracy, bias, *weights])
  mysql.cursor().execute("""INSERT INTO perceptron_weights (mood_couple, weight_accuracy, bias, duration_ms, danceability, acousticness, energy, liveness, valence, instrumentalness, tempo, speechiness, loudness) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",data)
  mysql.commit()

def test_weights(mysql, moods):
  weights = pd.read_sql_query("SELECT duration_ms, danceability, acousticness, energy, liveness, valence, instrumentalness, tempo, speechiness, loudness FROM perceptron_weights ORDER BY id DESC LIMIT 1", con = mysql).as_matrix()[0]
  bias = pd.read_sql_query("SELECT bias FROM perceptron_weights ORDER BY id DESC LIMIT 1", con = mysql).as_matrix()[0]
  X, Y, mood_couple = read_songs(mysql, moods)
  for song in list(zip(X,Y)):
    dictionary = {1: "happy", -1: "sad"}
    if array_dot(song[0], weights) + bias > 0:
      print("Happy - {}".format(dictionary[song[1]]))
    else:
      print("Sad - {}".format(dictionary[song[1]]))
  return None
