from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy import stats
import numpy as np
import pandas as pd

class PlaylistTraining:
  def __init__(self, mysql):
    self.mysql = mysql

## STORING METHODS

  def pc_to_db(self, pc):
    cursor = self.mysql.cursor()
    for key, value in pc['ev'].items():
      cursor.execute("""INSERT INTO pcs (version, param, ev, variance, created_at) VALUES (%s,%s,%s,%s, NOW())""",(pc["ver"], key, value, pc["var"]))
    self.mysql.commit()

  # def kluster_to_db(self, kluster):
  #   cursor = self.mysql.cursor()
  #   for key, value in pc['ev'].items():
  #     cursor.execute("""INSERT INTO pcs (version, param, ev, variance, created_at) VALUES (%s,%s,%s,%s, NOW())""",(pc["ver"], key, value, pc["var"]))
  #   self.mysql.commit()

## LOADING METHODS

  def load_training(self):
    dirty_training_df = pd.read_sql_query("SELECT * FROM tracks WHERE training = TRUE", con = self.mysql, index_col = ["spotify_id", "mood"]).drop("created_at", 1).drop("training", 1)
    return self.normalize(dirty_training_df)

  def last_version(self, variable):
    cursor = self.mysql.cursor()
    cursor.execute("SELECT MAX(version) FROM {} AS version".format(variable))
    return cursor.fetchone()[0]

## ANALYTIC METHODS

  def normalize(self, df):
    denominators = df.max() - df.min()
    zeroes = [x for x in denominators if x == 0]
    if len(zeroes) > 0:
      return df
    else:
      return (df - df.mean()) / (df.max() - df.min())

  def klusterize(self, df, n_kl = 4):
    kmeans = KMeans(init='k-means++', n_clusters=n_kl, n_init=10)
    return kmeans.fit(df)

  def pca(self, df, n_pc = 3):
    pca = PCA(n_components=n_pc)
    return pca.fit(df)

## TRAINING METHODS

  def create_training_set(self, n_pc = 4, ver = 1):
    df = self.load_training()
    pca = self.pca(df)
    columns = df.columns
    variances = pca.explained_variance_ratio_
    for idx, component in enumerate(pca.components_):
      pc = {'ver': ver, 'var': variances[idx], 'ev': dict(zip(columns, component))}
      self.pc_to_db(pc)

