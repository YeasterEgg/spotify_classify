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
    self.mysql = MySQLdb.connect(user = self.DB_SETTINGS['user'], db = self.DB_SETTINGS['name'], host = self.DB_SETTINGS['host'])
    self.df = pd.read_sql_query("SELECT * FROM tracks", con = self.mysql, index_col = ["spotify_id"]).drop("created_at", 1).drop("training", 1).drop("id", 1)
    self.gn = ["sad","happy","energy"]
    self.gcn = "mood"
    self.fvn = 4
    self.swp = False
    self.tss = 0.1
    self.prepare_df()
    return self

  def draw_corr_matrix(self):
    plt.imshow(self.dummy_df.corr(), cmap='hot', interpolation='nearest')
    plt.savefig('./plots/cor_matrix.png', bbox_inches='tight')
    plt.close()

  def draw_scatter_matrix(self):
    pd.tools.plotting.scatter_matrix(self.df)
    plt.savefig('./plots/scatter_matrix.png', bbox_inches='tight')
    plt.close()

  def perform(self):
    if not self.coefficients:
      if self.swp:
        self.coefficients = self.generate_first_coefficients(self.variables)
      else:
        self.coefficients = self.generate_first_coefficients(self.variables)
    else:
      self.slightly_move(self.coefficients)
    for variable in self.variables:
      self.df[variable].update(self.df[variable] * self.coefficients[variable])
    self.clusters = self.clusterize(self.df, self.gn, [self.gcn])

  def perform_after_pca(self):
    rotated_df = self.pca_rotation(self.df, self.pc_number, [self.gcn])

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

  def slightly_move(self, coefficients):
    return coefficients

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

test = MachineLearning().load_test()
