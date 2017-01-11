from sanic import Sanic
from sanic.response import json, html
from jinja2 import Environment, FileSystemLoader
import json as json_parser
import os

import mood as ml
import config as cfg

app = Sanic(__name__)
app.static('/public', './public')

env = Environment(loader=FileSystemLoader('./templates/.'))

@app.route('/')
async def home(request):
  return html(env.get_template('home.j2').render())

@app.route("/d3js")
async def d3js(request):
  return html(env.get_template('d3js.j2').render())

@app.route('/playlist')
async def playlist_post(request):
  if not request.json or not "playlist" in request.json or not "token" in request.json:
    return json({'error': 'Json missing or not formatted correctly!'})

  body = json_parser.loads(request.json)
  token = body['token']['token']
  ts = body['token']['ts']

  if cfg.authorize(token, ts):
    playlist = body['playlist']
  else:
    return json({'error': 'Token not Valid!', 'token': token})

  result = ml.playlist_analyzer.analyze_playlist(playlist, ["happy", "sad"])

  if result:
    return json({"result": "OK", "clusters": result})
  else:
    return json({"NOPE"})

@app.route("/songs")
async def songs(request):
  cursor = cfg.db.mysql().cursor()
  limit = None
  if ("limit" in request.args) and request.args["limit"][0].isdigit():
    limit = request.args["limit"][0]
  songs = cfg.db.training_to_json(limit = limit or None)
  return json(songs)

@app.route('/<fallback>')
async def fallback(request, fallback):
  return html("There is nothing here in {}! Go back to <a href='/'>HERE</a> where you can see the content.".format(fallback))

if __name__ == '__main__':
  app.run(debug=True, port=4000)
