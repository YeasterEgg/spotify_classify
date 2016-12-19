import os
import db
import MySQLdb
import pandas as pd
from sklearn import model_selection
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

DB_SETTINGS = db.DatabaseInterface().return_options()

def read_database(moods_tuple):
  mysql = MySQLdb.connect(user = DB_SETTINGS['user'], db = DB_SETTINGS['name'], host = DB_SETTINGS['host'])
  return pd.read_sql_query("SELECT * FROM tracks WHERE mood in {} AND `training` = 1".format(moods_tuple), con = mysql, index_col = ["spotify_id"]).drop("created_at", 1).drop("training", 1).drop("id", 1)

def calculate_parameters(moods = ("happy", "sad")):
  moods_tuple = tuple(moods)
  filename = "_".join(mood for mood in moods_tuple)
  df = read_database(moods_tuple)
  X = df.values[:,1:10]
  Y = df.values[:,0]
  lda = LinearDiscriminantAnalysis()
  lda.fit(X, Y)
  save_model(lda, filename)

def save_model(lda_fit, filename):
  current_path = os.getcwd()
  filename = os.path.join(current_path, "models", "filename.pkl")
  with open(filename, 'wb') as fo:
    joblib.dump(lda_fit, fo)

def predict_playlist(moods = ("happy", "sad"))
  predictions = lda.predict(X_validation)
  print(accuracy_score(self.Y_validation, self.predictions))
  print(confusion_matrix(self.Y_validation, self.predictions))
  print(classification_report(self.Y_validation, self.predictions))
