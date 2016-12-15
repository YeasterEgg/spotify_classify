from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import MySQLdb
import db

## MY FIRST EXPERIMENT WITH MACHINE LEARNING
## How it should it work:
## Receive a song, evaluate it and decide which mood it evocates.
## I want to use Machine Learning to create a reliable rotation of the data I can retrieve from Spotify.
## I need to start from the axiom that these informations will be enough to safely infer the mood of a song.

## Since there are plenty of "moody" playlists, I'll use them as training set, with a random sample of 10% as
## testing set.

DB_SETTINGS = db.DatabaseInterface().return_options()

def load_test(self):
  coefficients = generate_first_coefficients(self.variables)
  self.mysql = MySQLdb.connect(user = self.DB_SETTINGS['user'], db = self.DB_SETTINGS['name'], host = self.DB_SETTINGS['host'])
  self.gn = ["sad","happy","energy"]
  self.gcn = "mood"
  self.fvn = 4
  self.swp = False
  self.tss = 0.2
  self.prepare_df()
  return self

def connect_to_db(db, user, host):
  return MySQLdb.connect(user = user, db = db, host = host)

def read_dataframe(connection, table, index_name, droppable_columns):
  whole_df = pd.read_sql_query("SELECT * FROM {}".format(table), con = connection, index_col = [index_name])
  for column in droppable_columns:
    whole_df = whole_df.drop(column, 1)
  return whole_df

def perform_test:
  return read_dataframe(connect_to_db(DB_SETTINGS['name'], DB_SETTINGS['user'], DB_SETTINGS['host']),
                        "tracks",
                        "spotify_id",
                        ["created_at", "training", "id"]
                        )


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
    self.training_df = self.df[self.df.index.isin(dropped_indices)]
    self.df = self.df.drop(dropped_indices)
    self.dummy_df = pd.get_dummies(self.df)

def clusterize(self, df, groups, droppable_columns = []):
  cluster_number = len(groups)
  kmeans = KMeans(init='k-means++', n_clusters=cluster_number, n_init=10)
  return kmeans.fit(df.drop(droppable_columns, axis=1))

## ANALYTIC METHODS

def normalize(self, df, droppable_columns = []):
  integer_df = df.drop(droppable_columns, axis=1)
  string_df = df[droppable_columns]
  denominators = integer_df.max() - integer_df.min()
  zeroes = [x for x in denominators if x == 0]
  if len(zeroes) > 0:
    normalized_df = integer_df
  else:
    normalized_df = (integer_df - integer_df.mean()) / (integer_df.max() - integer_df.min())
  return pd.concat([normalized_df, string_df], axis=1)

## PLOTTING METHODS

def draw_corr_matrix(self):
  plt.imshow(self.dummy_df.corr(), cmap='hot', interpolation='nearest')
  plt.savefig('./plots/cor_matrix.png', bbox_inches='tight')
  plt.close()

def draw_scatter_matrix(self):
  pd.tools.plotting.scatter_matrix(self.df)
  plt.savefig('./plots/scatter_matrix.png', bbox_inches='tight')
  plt.close()

test = MachineLearning().load_test()
