import json
from sklearn.decomposition import PCA

class PlaylistAnalyzer:
  def __init__(self, playlist):
    self.playlist = playlist

  def return_playlist(self):
    return self.playlist

  def parse_playlist(self):
    self.tracks = self.playlist["songlist"]
    name = self.playlist["_id"]
    self.tracks = []
    for key, value in self.tracks.items():
      parsed_track = self.manage_track(value)
      self.tracks.append(parsed_track)

  def manage_track(self, track):
    parsed = {}
    parsed["spotifyId"]        = track["spotifyId"]
    parsed["artist"]           = track["artist"]
    parsed["album"]            = track["album"]
    parsed["name"]             = track["name"]
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

  def check_correctness(self):
    return True

  def pca(self):
