import hug
import json as json_parser
import os
import mood as ml
import db_config as cfg
import pdb

@hug.get("/happy_birthday")
async def home(request):
  return "ciao"

@hug.post('/playlist')
def playlist_post(body):
  if not body or not "playlist" in body or not "token" in body:
    return {'error': 'Json missing or not formatted correctly!'}

  body = json_parser.loads(body)
  token = body['token']['token']
  ts = body['token']['ts']

  if cfg.authorize(token, ts):
    playlist = body['playlist']
  else:
    return {'error': 'Token not Valid!', 'token': token}

  result = ml.playlist_analyzer.analyze_playlist(playlist, ["happy", "sad"])

  if result:
    return {"result": "OK", "clusters": result}
  else:
    return {"NOPE"}

@hug.get("/songs")
def songs(limit: hug.types.number = None):
  cursor = cfg.db.mysql().cursor()
  if limit:
    songs = cfg.db.training_to_json(limit)
  else:
    songs = cfg.db.training_to_json(None)
  return songs
