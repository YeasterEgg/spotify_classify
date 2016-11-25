from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import pandas as pd
import numpy as np
import os
import MySQLdb
import db


class IterativeGrouping:

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
    self.df = pd.read_sql_query("SELECT * FROM tracks", con = self.mysql, index_col = ["spotify_id"]).drop("created_at", 1).drop("training", 1)
    self.gn = ["sad","happy","energy"]
    self.gcn = "mood"
    self.fvn = 4
    self.swp = False
    self.tss = 0.1
    self.prepare_df()
    return self

  def perform(self):
    if not self.coefficients:
      if swp:
        self.coefficients = self.generate_first_coefficients(self.variables)
      else:
        # HERE TO BE USED A ROTATED SYSTEM VIA PCA
        self.coefficients = self.generate_first_coefficients(self.variables)
    else:
      self.slightly_move(self.coefficients)
    for variable in self.variables:
      self.df[variable].update(self.df[variable] * self.coefficients[variable])
    self.clusters = self.clusterize(self.df, self.variables)

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
      self.variables = self.df.drop([self.gcn, "id"], axis=1).columns
      dropped_amount = int(self.tss * self.df.shape[0])
      dropped_indices = np.random.choice(self.df.index, dropped_amount, replace=False)
      self.training_df = self.df[self.df.index.isin(dropped_indices)]
      self.df = self.df.drop(dropped_indices)

  def slightly_move(self, coefficients):
    return coefficients

  def clusterize(self, df, variables):
    cluster_number = len(variables)
    kmeans = KMeans(init='k-means++', n_clusters=n_kl, n_init=10)
    return kmeans.fit(df)

## LOADING METHODS

  def available_moods(self):
    self.cursor.execute("SELECT DISTINCT mood FROM tracks")
    moods = self.cursor.fetchall()
    return [i[0] for i in moods]

## ANALYTIC METHODS

  def store_klusters(self,clusters):
    for cluster in clusters:
      self.kluster_to_db(cluster)

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

## TRAINING METHODS

  def create_simple_training_set(self, droppable_columns = ["mood", "id"]):
    df = self.load_training()
    training_pca = self.calculate_pcs(df, droppable_columns)
    self.save_current_pca(training_pca)
    pc_version = self.current_pca_version()
    clusters = []
    for mood in self.available_moods():
      cluster = {}
      cluster["name"] = mood
      mood_df = df[df["mood"] == mood]
      clean_mood_df = mood_df.drop(droppable_columns, axis=1)
      transformed_df = pd.DataFrame(training_pca.transform(clean_mood_df))
      print(transformed_df)
      for column in transformed_df:
        coords = sum(transformed_df[column]) / len(transformed_df[column])
        variable = "pc" + str(column + 1)
        cluster[variable] = coords
      cluster["version"] = pc_version
      clusters.append(cluster)
    self.store_klusters(clusters)

  def clean_outliers(self, max_loops = 0):
    pass
