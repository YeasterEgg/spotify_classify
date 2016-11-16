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
    tracks = []
    for key, value in self.tracks.items():
      tracks.append(value)
    with open(name + ".json", 'w') as outfile:
      json.dump(tracks, outfile)
    return name

  def check_correctness(self):
    return True
