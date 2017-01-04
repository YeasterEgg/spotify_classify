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
#   weight_accuracy DECIMAL(12,8) NULL,
#   duration_ms DECIMAL(12,8) NULL,
#   danceability DECIMAL(12,8) NULL,
#   energy DECIMAL(12,8) NULL,
#   liveness DECIMAL(12,8) NULL,
#   valence DECIMAL(12,8) NULL,
#   instrumentalness DECIMAL(12,8) NULL,
#   tempo DECIMAL(12,8) NULL,
#   speechiness DECIMAL(12,8) NULL,
#   loudness DECIMAL(12,8) NULL,
#   acousticness DECIMAL(12,8) NULL,
#   PRIMARY KEY (id)
#   );

import os
from os.path import join, dirname
from dotenv import load_dotenv
import MySQLdb

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def mysql():
  if os.getenv("ENV")=="production":
    return MySQLdb.connect(user = "root", db = "py_mood", host = "localhost", passwd = os.getenv("DB_PASSWORD"))
  else:
    return MySQLdb.connect(user = "root", db = "py_mood", host = "localhost")
