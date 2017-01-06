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

def read_database(mysql, moods_tuple, threshold = 1):
  return pd.read_sql_query("SELECT spotify_id, mood, duration_ms, danceability, acousticness, energy, liveness, valence, instrumentalness, tempo, speechiness, loudness FROM tracks WHERE mood in {} AND count > {}".format(moods_tuple, threshold), con = mysql, index_col = ["spotify_id"])

def evaluate_models(mysql, moods, test_size = 0.2, seed = 42, num_folds = 50, scoring = "accuracy"):
  moods_tuple = tuple(sorted(moods))
  X_train, X_validation, Y_train, Y_validation = load_db(mysql, moods_tuple, test_size, seed)
  num_instances = len(X_train)
  results, names, models = [], [], []
  models.append(('LR', LogisticRegression()))
  models.append(('LDA', LinearDiscriminantAnalysis()))
  models.append(('KNN', KNeighborsClassifier()))
  models.append(('CART', DecisionTreeClassifier()))
  models.append(('NB', GaussianNB()))
  models.append(('SVM', SVC()))
  for name, model in models:
    kfold = model_selection.KFold(n_splits=num_folds, random_state=seed)
    cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)

def load_db(mysql, moods_tuple, test_size, seed):
  df = read_database(mysql, moods_tuple)
  array = df.values
  X = array[:,1:10]
  Y = array[:,0]
  return model_selection.train_test_split(X, Y, test_size=test_size, random_state=seed)

def simply_the_best(mysql, moods, test_size = 0.2, seed = 42):
  moods_tuple = tuple(sorted(moods))
  X_train, X_validation, Y_train, Y_validation = load_db(mysql, moods_tuple, test_size, seed)
  lda = LinearDiscriminantAnalysis()
  lda.fit(X_train, Y_train)
  predictions = lda.predict(X_validation)
  print(accuracy_score(Y_validation, predictions))
  print(confusion_matrix(Y_validation, predictions))
  print(classification_report(Y_validation, predictions))

