import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

def calculate_parameters(mysql, limit = False):
  query = "SELECT spotify_id, mood, acousticness, danceability, duration_ms, energy, instrumentalness, liveness, loudness, speechiness, tempo, valence FROM tracks WHERE mood in ('happy','sad') AND active = 1 AND good_for_model = 1"
  if limit:
    query += " LIMIT {}".format(limit)
  df = pd.read_sql_query(query, con = mysql, index_col = ["spotify_id"])
  X = df.drop("mood",1)
  Y = df[["mood"]]
  X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=.2)

  clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(5, 2), random_state=1)

  clf.fit(X_train, y_train)
  score = clf.score(X_test, y_test)

  clf.fit(X, Y)
  return clf
