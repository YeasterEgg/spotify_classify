# CREATE TABLE tracks (
#   id INT NOT NULL AUTO_INCREMENT,
#   spotify_id VARCHAR(45) NOT NULL,
#   mood VARCHAR(45) NOT NULL,
#   duration_ms BIGINT NULL,
#   danceability DECIMAL(12,8) NULL,
#   energy DECIMAL(12,8) NULL,
#   liveness DECIMAL(12,8) NULL,
#   valence DECIMAL(12,8) NULL,
#   instrumentalness DECIMAL(12,8) NULL,
#   tempo DECIMAL(12,8) NULL,
#   speechiness DECIMAL(12,8) NULL,
#   loudness DECIMAL(12,8) NULL,
#   acousticness DECIMAL(12,8) NULL,
#   count BIGINT 0,
#   PRIMARY KEY (id, spotify_id)
#   );

# CREATE TABLE perceptron_weights (
#   id INT NOT NULL AUTO_INCREMENT,
#   mood_couple VARCHAR(45) NOT NULL,
#   weight_accuracy DECIMAL(18,8) NULL,
#   bias DECIMAL(18,8) NULL,
#   duration_ms DECIMAL(18,8) NULL,
#   danceability DECIMAL(18,8) NULL,
#   energy DECIMAL(18,8) NULL,
#   liveness DECIMAL(18,8) NULL,
#   valence DECIMAL(18,8) NULL,
#   instrumentalness DECIMAL(18,8) NULL,
#   tempo DECIMAL(18,8) NULL,
#   speechiness DECIMAL(18,8) NULL,
#   loudness DECIMAL(18,8) NULL,
#   acousticness DECIMAL(18,8) NULL,
#   PRIMARY KEY (id)
#   );

import os
from dotenv import load_dotenv
import MySQLdb

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

def mysql():
  if os.getenv("ENV")=="production":
    return MySQLdb.connect(user = "root", db = "py_mood", host = "localhost", passwd = os.getenv("DB_PASSWORD"))
  else:
    return MySQLdb.connect(user = "root", db = "py_mood", host = "localhost")

def training_to_json(limit):
  sql = "SELECT spotify_id, mood, count, duration_ms, danceability, energy, liveness, valence, instrumentalness, tempo, speechiness, loudness, acousticness FROM tracks ORDER BY count DESC"
  if limit:
    sql += " LIMIT {}".format(limit)
  cursor = mysql().cursor()
  count = cursor.execute(sql)

  header = ["spotify_id", "mood", "count", "duration_ms", "danceability", "energy", "liveness", "valence", "instrumentalness", "tempo", "speechiness", "loudness", "acousticness"]
  stats = {variable: 0 for variable in header[2:]}
  stats["total_songs"] = 0
  rows = []
  for result in cursor.fetchall():
    stats["total_songs"] += 1
    song = {
      "spotify_id": result[0],
      "mood": result[1],
      "count": result[2],
      "duration_ms": result[3],
      "danceability": result[4],
      "energy": result[5],
      "liveness": result[6],
      "valence": result[7],
      "instrumentalness": result[8],
      "tempo": result[9],
      "speechiness": result[10],
      "loudness": result[11],
      "acousticness": result[12]
    }
    rows.append(song)
    for key, value in song.items():
      if key in stats:
        stats[key] += value
  return { "header": header, "data": rows, "stats": stats }
