# CREATE TABLE `tracks` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `spotify_id` varchar(45) NOT NULL,
#   `title` varchar(255) NOT NULL,
#   `artist` varchar(255) NOT NULL,
#   `mood` varchar(45) NOT NULL,
#   `popularity` bigint(20) DEFAULT NULL,
#   `duration_ms` bigint(20) DEFAULT NULL,
#   `danceability` decimal(12,8) DEFAULT NULL,
#   `energy` decimal(12,8) DEFAULT NULL,
#   `liveness` decimal(12,8) DEFAULT NULL,
#   `valence` decimal(12,8) DEFAULT NULL,
#   `instrumentalness` decimal(12,8) DEFAULT NULL,
#   `tempo` decimal(12,8) DEFAULT NULL,
#   `speechiness` decimal(12,8) DEFAULT NULL,
#   `loudness` decimal(12,8) DEFAULT NULL,
#   `acousticness` decimal(12,8) DEFAULT NULL,
#   `count` bigint(20) DEFAULT NULL,
#   PRIMARY KEY (`id`,`spotify_id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

import os
import MySQLdb
from dotenv import load_dotenv
from os.path import dirname, join

current_path = dirname(__file__)
dotenv_path = join(current_path, '.env')
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
