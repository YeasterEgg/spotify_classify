from sanic import Sanic
from sanic.response import html, json
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
from os.path import dirname, join
import numpy as np
import asyncio
import aiohttp
import pdb

import json as json_parser
import mood as ml
import db_config as cfg

current_path = dirname(__file__)
dotenv_path = join(current_path, '.env')
load_dotenv(dotenv_path)

app = Sanic(__name__)
app.static('/build', './build')

env = Environment(loader=FileSystemLoader('./build/.'))

@app.route("/")
async def home(request):
  url = "http://127.0.0.1:4000/visited_website?site=pymood" if (app.debug == True) else "https://grokked.it/visited_website?site=pymood"
  asyncio.ensure_future(message_in_a_bottle(url))
  return html(env.get_template('index.html').render())

@app.route("/songs")
async def songs(request):
  cursor = cfg.db.mysql().cursor()
  if ("limit" in request.args) and request.args["limit"][0].isdigit():
    rd = cfg.db.training_to_json(request.args["limit"][0])
  else:
    rd = cfg.db.training_to_json(None)
  cov_matrix = []
  for variable in rd["headers"]["numeric"]:
    variable_row = []
    mn, mx = get_extremes(rd["data"], variable)
    for song in rd["data"]:
      song["values"][variable] = (float(song["values"][variable]) - mn) / (mx - mn)
      variable_row.append(song["values"][variable])
    cov_matrix.append(variable_row)
  rd["cov"] = np.corrcoef(cov_matrix)
  return json(rd)

@app.route('/playlist')
def playlist_post(request):
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

async def message_in_a_bottle(url):
  r = await aiohttp.get(url)
  r.close()

def get_extremes(obj_list, variable):
  mn = min(obj_list, key = lambda x: float(x["values"][variable]))["values"][variable]
  mx = max(obj_list, key = lambda x: float(x["values"][variable]))["values"][variable]
  return float(mn), float(mx)

loop = asyncio.get_event_loop()

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=5000, debug=True, loop=loop)
