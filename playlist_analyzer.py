import pandas as pd

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

  def load_tracks(self):
    dirty_df = pd.read_sql_query("SELECT * FROM tracks", con = self.mysql, index_col = ["spotify_id", "mood"]).drop("created_at", 1).drop("training", 1)
    return self.normalize(dirty_df)

  def last_version(self):
    self.cursor.execute("SELECT MAX(version) FROM pcs AS version")
    version = self.cursor.fetchone()[0]
    if version is not None:
      return version
    else:
      return 0

  def load_pcs(self):
    self.cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name LIKE 'pcs'")
    columns = [column[0] for column in self.cursor.fetchall()]
    last_version = self.last_version()
    self.cursor.execute("SELECT * FROM pcs WHERE version = '{}'".format(last_version))
    raw_pcs = self.cursor.fetchall()
    pcs = []
    for pc in raw_pcs:
      pc_hash = {}
      for idx, variable in enumerate(pc):
        pc_hash[columns[idx]] = variable
      pcs.append(pc_hash)
    return pcs

  def load_evs(self, pc_id):
    self.cursor.execute("SELECT param, coefficient FROM evs WHERE pc_id = {}".format(pc_id))
    raw_evs = self.cursor.fetchall()
    evs = []
    for ev in raw_evs:
      evs.append({"param":ev[0], "value": float(ev[1])})
    return evs


## STORING METHODS

  def track_to_db(self, track):
    if self.cursor.execute("SELECT * FROM tracks WHERE spotify_id = '{}' AND training = {}".format(track["spotify_id"], track["training"])):
      print("Track {} already known. Should increase its count.".format(track["spotify_id"]))
    else:
      self.cursor.execute("""INSERT INTO tracks (spotify_id, mood, duration_ms, danceability, acousticness, energy, liveness, valence, instrumentalness, tempo, speechiness, loudness, training, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, NOW())""",(track["spotify_id"], track["mood"], track["duration_ms"], track["danceability"], track["acousticness"], track["energy"], track["liveness"], track["valence"], track["instrumentalness"], track["tempo"], track["speechiness"], track["loudness"], track["training"]))
      self.mysql.commit()

## ANALYSIS METHODS

  def pca_playlist(self, playlist):
    pcs = self.load_pcs()
    for track in playlist:
      self.rotate_track(track, pcs)

  def rotate_track(self,track, pcs):
    rotated_track = {"track_id": track["spotify_id"]}
    for pc in pcs:
      pc_rank = "pc"+ str(pc['rank'])
      evs = self.load_evs(pc["id"])
      pc_value = 0
      for ev in evs:
        pc_value += track[ev["param"]] * ev["value"]
      rotated_track[pc_rank] = pc_value
    print(rotated_track)
    return rotated_track


