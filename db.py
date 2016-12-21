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
#   training BOOL NULL,
#   PRIMARY KEY (id, spotify_id)
#   );

import os

class DatabaseInterface:

  DEFAULT_SETTINGS = {
      'name': 'py_mood',
      'user': 'root',
      'host': 'localhost'
  }

  def __init__(self, options = DEFAULT_SETTINGS):
    self.options = self.DEFAULT_SETTINGS

  def return_options(self):
    return self.options
