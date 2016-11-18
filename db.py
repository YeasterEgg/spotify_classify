# CREATE TABLE tracks (
#   spotify_id VARCHAR(45) NOT NULL,
#   mood VARCHAR(45) NOT NULL,
#   duration_ms BIGINT NULL,
#   danceability DECIMAL(7,3) NULL,
#   energy DECIMAL(7,3) NULL,
#   liveness DECIMAL(7,3) NULL,
#   valence DECIMAL(7,3) NULL,
#   instrumentalness DECIMAL(7,3) NULL,
#   tempo DECIMAL(7,3) NULL,
#   speechiness DECIMAL(7,3) NULL,
#   loudness DECIMAL(7,3) NULL,
#   acousticness DECIMAL(7,3) NULL,
#   training BOOL NULL,
#   created_at TIMESTAMP NULL,
#   PRIMARY KEY (spotify_id)
#   );

# CREATE TABLE pcs (
#   id INT NOT NULL AUTO_INCREMENT,
#   variance DECIMAL(7,3) NULL,
#   params NVARCHAR(1000),
#   version INT,
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
