from sklearn.decomposition import PCA
from sklearn.externals import joblib
import pandas as pd
import os

class PlaylistAnalyzer:
  def __init__(self, mysql):
    self.mysql = mysql
    self.cursor = self.mysql.cursor()

## PARSING METHODS

  def parse_playlist(self, playlist):
    tracks = []
    for key, value in playlist["songlist"].items():
      track = self.parse_track(playlist, value)
      tracks.append(track)
    return tracks

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
    return parsed

## LOADING METHODS

  def load_training(self):
    return pd.read_sql_query("SELECT * FROM tracks WHERE training = TRUE", con = self.mysql, index_col = ["spotify_id"]).drop("created_at", 1).drop("training", 1)

  def last_version(self):
    return 0

## STORING METHODS

  def track_to_db(self, track):
    if self.cursor.execute("SELECT * FROM tracks WHERE spotify_id = '{}' AND training = {}".format(track["spotify_id"], track["training"])):
      print("Track {} already known. Should increase its count.".format(track["spotify_id"]))
    else:
      self.cursor.execute("""INSERT INTO tracks (spotify_id, mood, duration_ms, danceability, acousticness, energy, liveness, valence, instrumentalness, tempo, speechiness, loudness, training, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, NOW())""",(track["spotify_id"], track["mood"], track["duration_ms"], track["danceability"], track["acousticness"], track["energy"], track["liveness"], track["valence"], track["instrumentalness"], track["tempo"], track["speechiness"], track["loudness"], track["training"]))
      self.mysql.commit()

## ANALYSIS METHODS

  def pca_playlist(self, playlist):
    current = os.getcwd()
    filename = os.path.join(current, "pca_model", "pca.pkl")
    with open(filename, 'rb') as fo:
      pca = joblib.load(fo)
    return pca

