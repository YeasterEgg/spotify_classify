from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import pandas as pd
import numpy as np
import os
import MySQLdb
import db

db_settings = db.DatabaseInterface().return_options()
mysql = MySQLdb.connect(user = db_settings['user'], db = db_settings['name'], host = db_settings['host'])

class IterativeGrouping:

  def __init__(self, data_frame = None, group_names = ["sad","happy","energy"], group_column_name = "mood", final_variables_number = 4):
    if data_frame:
      self.df = data_frame
    else:
      self.df = pd.read_sql_query("SELECT * FROM tracks", con = mysql, index_col = ["spotify_id"]).drop("created_at", 1).drop("training", 1)
    self.gn = group_names
    self.gcn = group_column_name
    self.fvn = final_variables_number

  def perform_after_pca(self):
    rotated_df = self.pca_rotation(self.df, self.pc_number, [self.gcn])

  def first_iteration(self):
    coefficients = {}
    for column in self.df.drop([self.gcn, "id"], axis=1).columns:
      random_coefficient = np.random.choice([1,-1]) * np.random.random()
      coefficients[column] = random_coefficient
      print(random_coefficient)
      self.df[column].update(self.df[column] * random_coefficient)
    print(self.df)

  def pca_rotation(self, df, pc_number, droppable_columns = []):
    pca = PCA(n_components=pc_number)
    return pca.fit(df.drop(droppable_columns, axis=1))

## LOADING METHODS

  def available_moods(self):
    self.cursor.execute("SELECT DISTINCT mood FROM tracks")
    moods = self.cursor.fetchall()
    return [i[0] for i in moods]

## ANALYTIC METHODS

  def klusterize(self, df, n_kl = 3):
    kmeans = KMeans(init='k-means++', n_clusters=n_kl, n_init=10)
    return kmeans.fit(df)


  def store_klusters(self,clusters):
    for cluster in clusters:
      self.kluster_to_db(cluster)

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
