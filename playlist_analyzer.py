from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import db

class PlaylistAnalyzer:
  def __init__(self, playlist, training):
    self.training = training
    self.playlist = playlist
    self.tracks = []

  def parse_playlist(self):
    for key, value in self.tracks.items():
      parsed_track = self.parse_track(value)
      self.tracks.append(parsed_track)

  def parse_track(self, track):
    parsed = {}
    parsed["spotifyId"]        = track["spotifyId"]
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

  def save_to_db(self):
    pass
