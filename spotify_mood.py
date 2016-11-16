from flask import Flask, jsonify, make_response, request
from flask_mysqldb import MySQL
import json

import playlist_analyzer as pa
import authorizer as auth
import db

app = Flask(__name__)
mysql = MySQL()

ENV = 'development'

app.config['MYSQL_DATABASE_USER'] = db.settings[ENV]['user']
app.config['MYSQL_DATABASE_PASSWORD'] = db.settings[ENV]['password']
app.config['MYSQL_DATABASE_DB'] = db.settings[ENV]['name']
app.config['MYSQL_DATABASE_HOST'] = db.settings[ENV]['host']
mysql.init_app(app)

VERSION = "v0.1"
def versionate_route(route):
  return ('/' + VERSION + '/' + route)


@app.route('/version', methods=['GET'])
def version():
  return VERSION

@app.route(versionate_route('test'), methods=['GET'])
def test():
  return "Tell me, how could i know?"

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found',
                                'available_pages': {
                                  '/version': 'GET - API Version',
                                  '/{version}/test': 'GET - Working Test',
                                  '/{version}/playlist': 'POST - Analyze Playlists'
                                  }
                                }), 404)

@app.route(versionate_route('playlist'), methods=['POST'])
def playlist_post():
  if not request.json:
    return jsonify({'error': 'WRONG'}), 400
  if not 'playlist' in request.json:
    return jsonify({'error': 'Json not correct'}), 400
  if not 'token' in request.json:
    return jsonify({'error': 'Needs a Token!'}), 403

  body = json.loads(request.json)
  token = body['token']['token']
  ts = body['token']['ts']
  authorized = auth.Authorizer(token, ts).correct()

  if not authorized:
    return jsonify({'error': 'Token not Valid!', 'token': token}), 403

  playlist = body['playlist']
  name = pa.PlaylistAnalyzer(playlist).parse_playlist()
  return jsonify(name), 201

@app.route(versionate_route('playlist_seed'), methods=['POST'])
def playlist_seed_post():
  if not request.json:
    return jsonify({'error': 'WRONG'}), 400
  if not 'playlist' in request.json:
    return jsonify({'error': 'Json not correct'}), 400
  if not 'token' in request.json:
    return jsonify({'error': 'Needs a Token!'}), 403

  body = json.loads(request.json)
  token = body['token']['token']
  ts = body['token']['ts']
  authorized = auth.Authorizer(token, ts).correct()

  if not authorized:
    return jsonify({'error': 'Token not Valid!', 'token': token}), 403

  playlist = body['playlist']
  name = pa.PlaylistAnalyzer(playlist).playlist_seed()
  return jsonify("THANKS!"), 201

@app.route(versionate_route('playlist'), methods=['GET'])
def playlist_get():
  return "This is a POST endpoint!"

if __name__ == '__main__':
  app.run(debug=True, port=4000)
