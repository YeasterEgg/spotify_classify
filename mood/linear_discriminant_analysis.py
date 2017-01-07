import os
import MySQLdb
import pandas as pd
from sklearn import model_selection
from sklearn.externals import joblib
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def read_database(mysql, moods_tuple, threshold = 1):
  return pd.read_sql_query("SELECT spotify_id, mood, acousticness, danceability, duration_ms, energy, instrumentalness, liveness, loudness, speechiness, tempo, valence FROM tracks WHERE mood in {} AND count > {}".format(moods_tuple, threshold), con = mysql, index_col = ["spotify_id"])

def calculate_parameters(mysql, moods = ("happy", "sad")):
  moods_tuple = tuple(sorted(moods))
  filename = "_".join(mood for mood in moods_tuple)
  df = read_database(mysql, moods_tuple)
  X = df.drop("mood",1)
  Y = df[["mood"]]
  lda = LinearDiscriminantAnalysis(n_components=4, store_covariance=True)
  lda.fit(X, Y.values.ravel())
  save_model(lda, filename)
  return list(lda.coef_[0])

def save_model(lda_fit, filename):
  current_path = os.getcwd()
  file = os.path.join(current_path, "models", "{}.pkl".format(filename))
  with open(file, 'wb') as fo:
    joblib.dump(lda_fit, fo)
