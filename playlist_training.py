from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pandas as pd

class PlaylistTraining:

  PCS_NUMBER = 4
  MOODS = ["happy", "sad", "energy"]

  def __init__(self, mysql):
    self.mysql = mysql

## STORING METHODS

  def pc_to_db(self, pc):
    cursor = self.mysql.cursor()
    cursor.execute("""INSERT INTO pcs (version, variance, created_at) VALUES (%s,%s, NOW())""",(pc["ver"], pc["var"]))
    pc_id = cursor.lastrowid
    for key, value in pc['ev'].items():
      cursor.execute("""INSERT INTO evs (pc_id, param, coefficient, created_at) VALUES (%s,%s,%s, NOW())""",(pc_id, key, value))
    self.mysql.commit()
    return pc_id

  def kluster_to_db(self, kluster):
    cursor = self.mysql.cursor()
    cursor.execute("""INSERT INTO klusters (version, name, pc1, pc2, pc3, pc4, created_at) VALUES (%s,%s,%s,%s,%s,%s, NOW())""",(kluster["version"], kluster["name"], kluster["pc1"], kluster["pc2"], kluster["pc3"], kluster["pc4"]))
    self.mysql.commit()

## LOADING METHODS

  def load_training(self, droppable_columns = []):
    dirty_training_df = pd.read_sql_query("SELECT * FROM tracks WHERE training = TRUE", con = self.mysql, index_col = ["spotify_id"]).drop("created_at", 1).drop("training", 1)
    return self.normalize(dirty_training_df, droppable_columns)

  def last_version(self, variable):
    cursor = self.mysql.cursor()
    cursor.execute("SELECT MAX(version) FROM {} AS version".format(variable))
    version = cursor.fetchone()[0]
    if version is not None:
      return version
    else:
      return 0

  def available_moods(self):
    cursor = self.mysql.cursor()
    cursor.execute("SELECT DISTINCT mood FROM tracks")
    moods = cursor.fetchall()
    return [i[0] for i in moods]

## ANALYTIC METHODS

  def normalize(self, df, droppable_columns = []):
    integer_df = df.drop(droppable_columns, axis=1)
    string_df = df[droppable_columns]
    denominators = integer_df.max() - integer_df.min()
    zeroes = [x for x in denominators if x == 0]
    if len(zeroes) > 0:
      normalized_df = integer_df
    else:
      normalized_df = (integer_df - integer_df.mean()) / (integer_df.max() - integer_df.min())
    return pd.concat([normalized_df, string_df], axis=1)

  def klusterize(self, df, n_kl = 3):
    kmeans = KMeans(init='k-means++', n_clusters=n_kl, n_init=10)
    return kmeans.fit(df)

  def calculate_pcs(self, df, droppable_columns = []):
    pca = PCA(n_components=self.PCS_NUMBER)
    return pca.fit(df.drop(droppable_columns, axis=1))

  def store_klusters(self,clusters):
    for cluster in clusters:
      self.kluster_to_db(cluster)

  def store_pcs(self, df, pcs):
    variances = pcs.explained_variance_ratio_
    columns = df.columns
    pc_version = int(self.last_version("pcs")) + 1
    ids = {}
    for idx, component in enumerate(pcs.components_):
      pc = {'ver': pc_version, 'var': variances[idx], 'ev': dict(zip(columns, component))}
      pc_id = self.pc_to_db(pc)
      ids["pc" + str(idx + 1)] = pc_id
    return {"pc_ids": ids, "pc_version":  pc_version}

## TRAINING METHODS

  def create_simple_training_set(self, droppable_columns = ["mood"]):
    df = self.load_training(droppable_columns)
    training_pcs = self.calculate_pcs(df, droppable_columns)
    pc_variables = self.store_pcs(df, training_pcs)
    pc_ids = pc_variables["pc_ids"]
    pc_version = pc_variables["pc_version"]
    clusters = []
    for mood in self.available_moods():
      cluster = {}
      cluster["name"] = mood
      mood_df = df[df["mood"] == mood]
      clean_mood_df = mood_df.drop(droppable_columns, axis=1)
      transformed_df = pd.DataFrame(training_pcs.transform(clean_mood_df))
      for column in transformed_df:
        coords = sum(transformed_df[column]) / len(transformed_df[column])
        variable = "pc" + str(column + 1)
        cluster[variable] = coords
      cluster["version"] = pc_version
      clusters.append(cluster)
    self.store_klusters(clusters)

  def clean_outliers(self, max_loops = 0):
    pass
