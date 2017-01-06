from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import pandas as pd
import os

def read_database(mysql, moods_tuple, threshold = 1):
  return pd.read_sql_query("SELECT spotify_id, mood, duration_ms, danceability, acousticness, energy, liveness, valence, instrumentalness, tempo, speechiness, loudness FROM tracks WHERE mood in {} AND count > {}".format(moods_tuple, threshold), con = mysql, index_col = ["spotify_id"])

def evaluate_models(mysql, moods, test_size = 0.2, seed = 42, num_folds = 50, scoring = "accuracy"):
  moods_tuple = tuple(sorted(moods))
  filename = "_".join(mood for mood in moods_tuple)
  current_path = os.getcwd()
  file = os.path.join(current_path, "models", "{}_results.log".format(filename))

  df = read_database(mysql, moods_tuple)
  array = df.values
  X = array[:,1:10]
  Y = array[:,0]
  X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=test_size, random_state=seed)
  num_instances = len(X_train)
  results, names, models = [], [], []
  models.append(('Logistic Regression', LogisticRegression()))
  models.append(('Linear Discrimination Analysis', LinearDiscriminantAnalysis()))
  models.append(('K-Neighbors Classifier', KNeighborsClassifier()))
  models.append(('Decision Tree Classifier', DecisionTreeClassifier()))
  models.append(('Gaussian NB', GaussianNB()))
  models.append(('SVC', SVC()))
  for name, model in models:
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)
    with open(file, 'a') as fo:
      fo.write(str("#"*70))
      fo.write(str("\n"))
      fo.write(str(name))
      fo.write(str("\n"))
      fo.write(str(accuracy_score(Y_validation, predictions)))
      fo.write(str("\n"))
      fo.write(str(confusion_matrix(Y_validation, predictions)))
      fo.write(str("\n"))
      fo.write(str(classification_report(Y_validation, predictions)))
      fo.write(str("\n"))

