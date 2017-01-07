from flask import Flask, jsonify, make_response, request
import json
import pdb

import mood as ml
import config as cfg

import MySQLdb
import os

app = Flask(__name__)

mysql = cfg.db.mysql()

VERSION = "v0.3"

def versionate_route(route):
  return ('/' + VERSION + '/' + route)

def authorize(request, object_name):
  if not request.json:
    return jsonify({'error': 'Missing Json'}), 400
  if not object_name in request.json:
    return jsonify({'error': 'Json missing necessary data.'}), 400
  if not 'token' in request.json:
    return jsonify({'error': 'Needs a Token!'}), 403
  body = json.loads(request.json)
  token = body['token']['token']
  ts = body['token']['ts']
  authorized = cfg.authorizer.Authorizer(token, ts).correct()
  if not authorized:
    return jsonify({'error': 'Token not Valid!', 'token': token}), 403
  return {'success': True, 'body': body[object_name]}

@app.route('/version', methods=['GET'])
def version():
  return VERSION

@app.route('/', methods=['GET'])
def root():
  return "Someday here you will be able to classify a single song! Anyhow, <a href='/404'>HERE</a> you can see the API endpoints."

@app.route(versionate_route('test'), methods=['GET'])
def test():
  return "Well maybe -working- test is a bit of an overstatement..."

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found',
                                'available_pages': {
                                  '/version': 'GET - API Version',
                                  '/{version}/test': 'GET - Working Test',
                                  '/{version}/reload_params?moods={mood1}_{mood2}': 'GET - Restart model creation',
                                  '/{version}/playlist': 'POST - Analyze Playlists',
                                  }
                                }), 404)

@app.route(versionate_route('playlist'), methods=['POST'])
def playlist_post():
  auth = authorize(request, "playlist")
  if auth['success']:
    playlist = auth['body']
  else:
    return auth
  result = ml.playlist_analyzer.analyze_playlist(playlist, ["happy", "sad"])
  if result:
    return jsonify({"result": "OK", "clusters": result}), 201
  else:
    return jsonify("NOPE"), 500

@app.route(versionate_route('playlist'), methods=['GET'])
def playlist_get():
  return "This is a POST endpoint!"

if __name__ == '__main__':
  app.run(debug=True, port=4000)
