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
#   `active` bool DEFAULT FALSE,
#   `good_for_model` bool DEFAULT TRUE,
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
  sql = "SELECT spotify_id, mood, artist, title, popularity, count, duration_ms, danceability, energy, liveness, valence, instrumentalness, tempo, speechiness, loudness, acousticness FROM tracks WHERE active IS TRUE ORDER BY RAND()"
  if limit:
    sql += " LIMIT {}".format(limit)
  cursor = mysql().cursor()
  count = cursor.execute(sql)
  headers = {
    "numeric":[
      "popularity",
      "count",
      "duration_ms",
      "danceability",
      "energy",
      "liveness",
      "valence",
      "instrumentalness",
      "tempo",
      "speechiness",
      "loudness",
      "acousticness"
    ],
    "textual":[
      "spotify_id",
      "mood",
      "artist",
      "title",
    ]
  }
  stats = {variable: 0 for variable in headers["numeric"]}
  stats["total_songs"] = 0
  rows = []
  for result in cursor.fetchall():
    stats["total_songs"] += 1
    song = {
      "spotify_id": result[0],
      "mood": result[1],
      "artist": result[2],
      "title": result[3],
      "values": {
        "popularity": result[4],
        "count": result[5],
        "duration_ms": result[6],
        "danceability": result[7],
        "energy": result[8],
        "liveness": result[9],
        "valence": result[10],
        "instrumentalness": result[11],
        "tempo": result[12],
        "speechiness": result[13],
        "loudness": result[14],
        "acousticness": result[15]
      }
    }
    rows.append(song)
    for key, value in song["values"].items():
      stats[key] += value
  return { "headers": headers, "data": rows, "stats": stats }
