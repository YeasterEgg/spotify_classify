from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy import stats
import numpy as np
import pandas as pd

class PlaylistAnalyzer:
  def __init__(self, mysql):
    self.mysql = mysql

## PARSING METHODS

  def parse_playlist(self, playlist):
    for key, value in playlist["songlist"].items():
      self.parse_track(playlist, value)
    return True

  def parse_track(self, playlist, track):
    parsed = {}
    parsed["spotify_id"]       = track["spotifyId"]
    parsed["mood"]             = playlist["mood"]
    parsed["training"]         = playlist["training"]
    parsed["duration_ms"]      = track["duration_ms"]
    parsed["danceability"]     = track["features"]["danceability"]
    parsed["acousticness"]     = track["features"]["acousticness"]
    parsed["energy"]           = track["features"]["energy"]
    parsed["liveness"]         = track["features"]["liveness"]
    parsed["valence"]          = track["features"]["valence"]
    parsed["instrumentalness"] = track["features"]["instrumentalness"]
    parsed["tempo"]            = track["features"]["tempo"]
    parsed["speechiness"]      = track["features"]["speechiness"]
    parsed["loudness"]         = track["features"]["loudness"]
    parsed["count"]            = 0
    self.track_to_db(parsed)

## STORING METHODS

  def pc_to_db(self, pc):
    cursor = self.mysql.cursor()
    for key, value in pc['ev'].items():
      cursor.execute("""INSERT INTO pcs (version, param, ev, variance, created_at) VALUES (%s,%s,%s,%s, NOW())""",(pc["ver"], key, value, pc["var"]))
    self.mysql.commit()

  def track_to_db(self, track):
    cursor = self.mysql.cursor()
    if cursor.execute("SELECT * FROM tracks WHERE spotify_id = '{}' AND training = {}".format(track["spotify_id"], track["training"])):
      print("Track {} already known. Should increase its count.".format(track["spotify_id"]))
    else:
      cursor = self.mysql.cursor()
      cursor.execute("""INSERT INTO tracks (spotify_id, mood, duration_ms, danceability, acousticness, energy, liveness, valence, instrumentalness, tempo, speechiness, loudness, training, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, NOW())""",(track["spotify_id"], track["mood"], track["duration_ms"], track["danceability"], track["acousticness"], track["energy"], track["liveness"], track["valence"], track["instrumentalness"], track["tempo"], track["speechiness"], track["loudness"], track["training"]))
      self.mysql.commit()

## LOADING METHODS

  def load_mood(self, mood):
    dirty_mood_df = pd.read_sql_query("SELECT * FROM tracks WHERE mood = '{}'".format(mood), con = self.mysql, index_col = ["spotify_id", "mood"]).drop("created_at", 1).drop("training", 1)
    return self.normalize(dirty_mood_df)

  def load_tracks(self):
    dirty_df = pd.read_sql_query("SELECT * FROM tracks", con = self.mysql, index_col = ["spotify_id", "mood"]).drop("created_at", 1).drop("training", 1)
    print(dirty_df)
    return self.normalize(dirty_df)

  def load_training(self):
    dirty_training_df = pd.read_sql_query("SELECT * FROM tracks WHERE training = TRUE", con = self.mysql, index_col = ["spotify_id", "mood"]).drop("created_at", 1).drop("training", 1)
    return self.normalize(dirty_training_df)

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

