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
