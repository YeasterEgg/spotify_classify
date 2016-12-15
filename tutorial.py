from sklearn import cross_validation
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
from pandas.tools.plotting import scatter_matrix
import numpy as np
import matplotlib.pyplot as plt
import os
import MySQLdb
import db

class MachineLearning:

  DB_SETTINGS = db.DatabaseInterface().return_options()

  def __init__(self,
               data_frame = None,
               mysql = None,
               group_names = None,
               group_column_name = None,
               final_variables_number = None,
               start_with_pca = False,
               training_set_size = None):
    self.df = data_frame
    self.mysql = mysql
    self.gn = group_names
    self.gcn = group_column_name
    self.fvn = final_variables_number
    self.swp = start_with_pca
    self.tss = training_set_size
    self.coefficients = False
    self.prepare_df()

  def load_test(self):
    self.coefficients = self.generate_first_coefficients(self.variables)
    self.mysql = MySQLdb.connect(user = self.DB_SETTINGS['user'], db = self.DB_SETTINGS['name'], host = self.DB_SETTINGS['host'])
    self.df = pd.read_sql_query("SELECT * FROM tracks", con = self.mysql, index_col = ["spotify_id"]).drop("created_at", 1).drop("training", 1).drop("id", 1)
    self.gn = ["sad","happy","energy"]
    self.gcn = "mood"
    self.fvn = 4
    self.swp = False
    self.tss = 0.2
    self.prepare_df()
    return self

  def generate_first_coefficients(self, variables):
    coefficients = {}
    for variable in variables:
      coefficient = np.random.choice([1,-1]) * np.random.random()
      coefficients[variable] = coefficient
    return coefficients

  def prepare_df(self):
    if self.df is None:
      self.variables = []
      self.training_df = None
    else:
      self.variables = self.df.drop([self.gcn], axis=1).columns
      dropped_amount = int(self.tss * self.df.shape[0])
      dropped_indices = np.random.choice(self.df.index, dropped_amount, replace=False)
      self.testing_df = self.df[self.df.index.isin(dropped_indices)]
      self.training_df = self.df.drop(dropped_indices)
      self.dummy_testing_df = pd.get_dummies(self.testing_df)
      self.dummy_training_df = pd.get_dummies(self.training_df)

## PLOTTING METHODS

  def draw_corr_matrix(self):
    plt.imshow(self.dummy_df.corr(), cmap='hot', interpolation='nearest')
    plt.savefig('./plots/cor_matrix.png', bbox_inches='tight')
    plt.close()

  def draw_scatter_matrix(self):
    pd.tools.plotting.scatter_matrix(self.df)
    plt.savefig('./plots/scatter_matrix.png', bbox_inches='tight')
    plt.close()

## TUTORIAL METHODS

  def validation_dataset(self):
    array = self.df.values
    X = array[:1,11]
    Y = array[:0]
    validation_size = self.tss
    seed = 8
    self.X_train, self.X_validation, self.Y_train, self.Y_validation = cross_validation.train_test_split(X, Y, test_size=validation_size, random_state=seed)

test = MachineLearning().load_test()
