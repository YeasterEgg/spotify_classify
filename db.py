# CREATE TABLE tracks (
#   id INT NOT NULL AUTO_INCREMENT,
#   spotify_id VARCHAR(45) NOT NULL,
#   mood VARCHAR(45) NOT NULL,
#   duration_ms BIGINT NULL,
#   danceability DECIMAL(9,6) NULL,
#   energy DECIMAL(9,6) NULL,
#   liveness DECIMAL(9,6) NULL,
#   valence DECIMAL(9,6) NULL,
#   instrumentalness DECIMAL(9,6) NULL,
#   tempo DECIMAL(9,6) NULL,
#   speechiness DECIMAL(9,6) NULL,
#   loudness DECIMAL(9,6) NULL,
#   acousticness DECIMAL(9,6) NULL,
#   training BOOL NULL,
#   created_at TIMESTAMP NULL,
#   PRIMARY KEY (id, spotify_id)
#   );

# CREATE TABLE pcs (
#   id INT NOT NULL AUTO_INCREMENT,
#   variance DECIMAL(9,6) NULL,
#   param VARCHAR(45) NOT NULL,
#   ev DECIMAL(9,6) NULL,
#   params VARCHAR(50),
#   version INT,
#   created_at TIMESTAMP NULL,
#   PRIMARY KEY (id)
#   );

# CREATE TABLE klusters (
#   id INT NOT NULL AUTO_INCREMENT,
#   name VARCHAR(45) NOT NULL,
#   pc1 DECIMAL(9,6) NULL,
#   pc2 DECIMAL(9,6) NULL,
#   pc3 DECIMAL(9,6) NULL,
#   pc4 DECIMAL(9,6) NULL,
#   version INT,
#   created_at TIMESTAMP NULL,
#   PRIMARY KEY (id)
#   );

import os

class DatabaseInterface:

  DEFAULT_SETTINGS = {
    'development': {
      'name': 'py_mood',
      'user': 'root',
      'password': None,
      'host': 'localhost'
    },
  }

  def __init__(self, options = DEFAULT_SETTINGS):
    env = os.getenv("ENV", "development")
    self.options = self.DEFAULT_SETTINGS[env]

  def return_options(self):
    return self.options
