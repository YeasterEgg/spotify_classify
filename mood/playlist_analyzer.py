import pandas as pd
import os
import MySQLdb
from sklearn.externals import joblib
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

## PARSING METHODS

def analyze_playlist(mysql, playlist):
  tracks = []
  cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
  for key, value in playlist.items():
    parsed_track = parse_track(playlist, value)
    tracks.append(parsed_track)
  return tracks

def parse_track(playlist, track):
  parsed = {}
  parsed["spotify_id"]       = track["spotifyId"]
  parsed["duration_ms"]      = track["duration_ms"]
  parsed["danceability"]     = track["features"]["danceability"]
  parsed["acousticness"]     = track["features"]["acousticness"]
  parsed["energy"]           = track["features"]["energy"]
  parsed["liveness"]         = track["features"]["liveness"]
  parsed["valence"]          = track["features"]["valence"]
  parsed["instrumentalness"] = track["features"]["instrumentalness"]
  parsed["tempo"]            = track["features"]["tempo"]
  parsed["speechiness"]      = track["features"]["speechiness"]
  parsed["loudness"]         = track["features"]["loudness"]
  return parsed

## ANALYSIS METHODS

def predict_playlist(playlist, moods = ("happy", "sad")):
  moods_tuple = tuple(sorted(moods))
  filename = "_".join(mood for mood in moods_tuple)
  lda = load_model(filename)
  print(playlist)
  df = pd.DataFrame(playlist).set_index("spotify_id")
  classification = lda.predict(df)
  result = {}
  for t, m in zip(list(df.index.values), list(classification)):
    result[t] = m
  return result

def load_model(filename):
  current_path = os.getcwd()
  file = os.path.join(current_path, "models", "{}.pkl".format(filename))
  with open(file, 'rb') as fo:
    pca = joblib.load(fo)
  return pca
