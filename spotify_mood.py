from flask import Flask, jsonify, make_response, request
import json
import MySQLdb
from os.path import join, dirname
from dotenv import load_dotenv

import playlist_analyzer as pa
import authorizer as auth
import db
import lda


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
db_settings = db.DatabaseInterface().return_options()
if db_settings['password']:
  mysql = MySQLdb.connect(user = db_settings['user'], db = db_settings['name'], host = db_settings['host'], password = db_settings['password'])
else:
  mysql = MySQLdb.connect(user = db_settings['user'], db = db_settings['name'], host = db_settings['host'])

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
  authorized = auth.Authorizer(token, ts).correct()
  if not authorized:
    return jsonify({'error': 'Token not Valid!', 'token': token}), 403
  return {'success': True, 'body': body[object_name]}

@app.route('/version', methods=['GET'])
def version():
  return VERSION

@app.route(versionate_route('test'), methods=['GET'])
def test():
  return "Well maybe -working- test is a bit of an overstatement..."

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
  auth = authorize(request, "playlist")
  if auth['success']:
    playlist = auth['body']
  else:
    return auth

  parsed_playlist = pa.analyze_playlist(mysql, playlist)
  result = pa.predict_playlist(parsed_playlist)
  print(result)
  if result:
    return jsonify({"result": "OK", "clusters": result}), 201
  else:
    return jsonify("NOPE"), 500

# SAFER ROUTE
# @app.route(versionate_route('reload_params'), methods=['POST'])
# def reload_params_post():
#   auth = authorize(request, "moods")
#   if auth['success']:
#     moods = auth['body']
#   else:
#     return auth

#   mood_tuple = tuple(moods)
#   result = lda.calculate_parameters(mood_tuple)
#   if result.any():
#     matrix = {}
#     for idx, line in enumerate(result):
#       matrix[idx] = list(line)
#     print(matrix)
#     return jsonify({"result": "OK", "covariance_matrix": matrix}), 201
#   else:
#     return jsonify("NOPE"), 500
# /SAFER ROUTE

@app.route(versionate_route('reload_params'), methods=['GET'])
def reload_params_get():
  if request.args.get('token') != auth.Authorizer.KEY:
    return jsonify({'error': "You are not authorized"}), 403
  mood_tuple = request.args.get('moods').split('_')
  result = lda.calculate_parameters(mood_tuple)
  if result:
    return jsonify({"result": "OK", "coefficients": result}), 201
  else:
    return jsonify("NOPE"), 500

@app.route(versionate_route('playlist'), methods=['GET'])
def playlist_get():
  return "This is a POST endpoint!"

if __name__ == '__main__':
  app.run(debug=True, port=4000)
