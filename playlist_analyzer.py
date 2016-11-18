from sklearn.decomposition import PCA
import numpy as np
from scipy import stats

class PlaylistAnalyzer:
  def __init__(self, playlist, training, mysql):
    self.training = training
    self.playlist = playlist["songlist"]
    self.tracks = []
    self.mysql = mysql
    self.mood = playlist["mood"]

  def parse_playlist(self):
    for key, value in self.playlist.items():
      parsed_track = self.parse_track(value)
      self.tracks.append(parsed_track)
    return self

  def parse_track(self, track):
    parsed = {}
    parsed["spotify_id"]       = track["spotifyId"]
    parsed["mood"]             = self.mood
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
    parsed["time_signature"]   = track["features"]["time_signature"]
    return parsed

  def store_to_db(self):
    for track in self.tracks:
      self.send_track_to_db(track)

  def send_track_to_db(self, track):
    cursor = self.mysql.cursor()
    if cursor.execute("SELECT * FROM tracks WHERE spotify_id = '{}'".format(track["spotify_id"])):
      # print("Track {} already known.".format(track["spotify_id"]))
    else:
      cursor = self.mysql.cursor()
      cursor.execute("""INSERT INTO tracks (spotify_id, mood, duration_ms, danceability, acousticness, energy, liveness, valence, instrumentalness, tempo, speechiness, loudness, time_signature) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(track["spotify_id"], track["mood"], track["duration_ms"], track["danceability"], track["acousticness"], track["energy"], track["liveness"], track["valence"], track["instrumentalness"], track["tempo"], track["speechiness"], track["loudness"], track["time_signature"]))
      self.mysql.commit()

  def load_mood(self, mood):
    cursor = self.mysql.cursor()
    cursor.execute("SELECT * FROM tracks WHERE mood = '{}'".format(mood))
    result = cursor.fetchall()
    return result

  def analyze_tracks(self, mood):
    pass

