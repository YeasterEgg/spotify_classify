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
      self.cursor.execute("SELECT * FROM tracks WHERE spotify_id = '{}' AND training = {}".format(value["spotifyId"], value["training"]))
      track = self.cursor.fetchone() or self.parse_track(playlist, value)
      print(track)
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

  def load_pca(self, version):
    current = os.getcwd()
    filename = os.path.join(current, "pca_model", "pca.pkl")
    with open(filename, 'rb') as fo:
      pca = joblib.load(fo)
    return pca

## STORING METHODS

  def track_to_db(self, track):
    self.cursor.execute("""INSERT INTO tracks (spotify_id, mood, duration_ms, danceability, acousticness, energy, liveness, valence, instrumentalness, tempo, speechiness, loudness, training, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, NOW())""",(track["spotify_id"], track["mood"], track["duration_ms"], track["danceability"], track["acousticness"], track["energy"], track["liveness"], track["valence"], track["instrumentalness"], track["tempo"], track["speechiness"], track["loudness"], track["training"]))
    self.mysql.commit()

## ANALYSIS METHODS

  def find_closer(self, klusters, pca, track):
    distances = []
    for kluster in klusters:
      for i in (0,1,2,3):
        print(kluster["pcs"])
        print(list(track))
    return 1

  def transform_df(self, playlist, pca):
    df = pd.DataFrame(playlist).drop(["mood", "training", "count"], axis=1)
    clean_df = df.set_index("spotify_id")
    transformed_df = pca.transform(clean_df)
    return pd.DataFrame(transformed_df, index=clean_df.index)

  def pca_playlist(self, playlist):
    version = self.last_version()
    pca = self.load_pca(version)
    klusters = self.load_klusters(version)
    transformed_df = self.transform_df(playlist, pca)
    klusterized = []
    for idx, row in transformed_df.iterrows():
      kluster = self.find_closer(klusters, pca, row)
      klusterized.append({"track": row, "kluster": kluster})
    return {"ciao": "ciao"}
