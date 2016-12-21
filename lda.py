import os
import db
import MySQLdb
import pandas as pd
from sklearn import model_selection
from sklearn.externals import joblib
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

DB_SETTINGS = db.DatabaseInterface().return_options()

def read_database(moods_tuple):
  mysql = MySQLdb.connect(user = DB_SETTINGS['user'], db = DB_SETTINGS['name'], host = DB_SETTINGS['host'])
  return pd.read_sql_query("SELECT spotify_id, mood, training, duration_ms, danceability, acousticness, energy, liveness, valence, instrumentalness, tempo, speechiness, loudness FROM tracks WHERE mood in {} AND `training` = 1".format(moods_tuple), con = mysql, index_col = ["spotify_id"])

def calculate_parameters(moods = ("happy", "sad")):
  moods_tuple = tuple(sorted(moods))
  filename = "_".join(mood for mood in moods_tuple)
  df = read_database(moods_tuple)
  X = df.drop("mood",1)
  Y = df[["mood"]]
  lda = LinearDiscriminantAnalysis(n_components=4, store_covariance=True)
  lda.fit(X, Y)
  save_model(lda, filename)
  return list(lda.coef_[0])

def save_model(lda_fit, filename):
  current_path = os.getcwd()
  file = os.path.join(current_path, "models", "{}.pkl".format(filename))
  with open(file, 'wb') as fo:
    joblib.dump(lda_fit, fo)

# def predict_playlist(playlist, moods = ("happy", "sad")):
#   moods_tuple = tuple(sorted(moods))
#   filename = "_".join(mood for mood in moods_tuple)
#   lda = load_model(filename)
#   df = pd
#   calssification = lda.predict(df.values[:,1:10])

# def load_model(filename):
#   current_path = os.getcwd()
#   file = os.path.join(current, "models", "{}.pkl".format(filename))
#   with open(file, 'rb') as fo:
#     pca = joblib.load(fo)
#   return pca
