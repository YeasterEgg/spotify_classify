import os
import requests
import base64
import csv
import pdb
from dotenv import load_dotenv
from os.path import dirname, join
import re
from collections import Counter

current_path = dirname(__file__)
dotenv_path = join(current_path, '.env')
load_dotenv(dotenv_path)

BATCH_MAX_SIZE = 50

current_path = dirname(__file__)

def token_url():
  return "https://accounts.spotify.com/api/token"

def search_url(query, obj_type = "playlist", limit = 50, offset = 0):
  return "https://api.spotify.com/v1/search?q={}&type={}&limit={}&offset={}".format(query, obj_type, limit, offset)

def playlist_url(user_id, playlist_id):
  return "https://api.spotify.com/v1/users/{}/playlists/{}/tracks".format(user_id, playlist_id)

def tracks_features_url(song_ids):
  ids = ','.join([str(id).strip("\n") for id in song_ids])
  return "https://api.spotify.com/v1/audio-features/?ids={}".format(ids)

def tracks_url(song_ids):
  ids = ','.join([str(id).strip("\n") for id in song_ids])
  return "https://api.spotify.com/v1/tracks/?ids={}".format(ids)

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

def access_token():
  payload = { 'grant_type': 'client_credentials'}
  auth_header = base64.b64encode(str(client_id + ':' + client_secret).encode())
  headers = {'Authorization': 'Basic %s' % auth_header.decode()}
  response = requests.post(token_url(), data=payload, headers=headers, verify=True)
  token_info = response.json()
  return token_info

def recover_playlist_from_query(mood, url = None, counter = 0):
  result = requests.get(url or search_url(mood))
  if result.status_code == 200:
    next_url = result.json()["playlists"]["next"]
    print("{}%".format((result.json()["playlists"]["offset"] * 100) / result.json()["playlists"]["total"]))
    with open("{}/lists/{}.txt".format(current_path, mood), "a") as file:
      for playlist in result.json()["playlists"]["items"]:
        file.write(playlist["tracks"]["href"])
        file.write("\n")
    if next_url is not None:
      recover_playlist_from_query(mood, next_url, counter = counter + 1)
  return "{}/lists/{}.txt".format(current_path, mood)

def recover_tracks_from_playlists(mood):
  playlists_filename = "{}/lists/{}.txt".format(current_path, mood)
  playlists_no = count_lines(playlists_filename)
  headers = {'Authorization': 'Bearer ' + access_token()["access_token"] }
  tracks_filename = "tracks_{}.txt".format(mood)
  counter = 0
  with open("{}/lists/{}.txt".format(current_path, mood), "r") as playlists:
    with open("{}/lists/{}".format(current_path, tracks_filename), "a") as tracks:
      for line in playlists:
        print("{}%".format((counter * 100) / playlists_no))
        href = line.strip("\n")
        counter = counter + 1
        parse_playlist_tracks(href, tracks, headers)
  return "{}/lists/{}".format(current_path, tracks_filename)

def parse_playlist_tracks(playlist_href, tracks_file, headers):
  result = requests.get(playlist_href, headers = headers)
  if result.status_code == 200:
    next_url = result.json()["next"]
    for track in result.json()["items"]:
      if (track["track"] is not None) and (track["track"]["id"] is not None):
        tracks_file.write(track["track"]["id"])
        tracks_file.write("\n")
    if next_url is not None:
      parse_playlist_tracks(next_url, tracks_file, headers)

def count_lines(filename):
  return sum(1 for line in open(filename))

def insert_songs_in_db(mood, mysql):
  tracks_file = "{}/lists/tracks_{}.txt".format(current_path, mood)
  lines = [i.strip() for i in open(tracks_file, "r").readlines()]
  songs = dict(Counter(lines))
  batch_size = 10000
  [write_batch_to_db(list(songs.items())[i:i+batch_size], mysql, mood) for i in range(0, len(songs), batch_size)]
  mysql.commit()

def write_batch_to_db(batch, mysql, mood):
  cursor = mysql.cursor()
  raw_sql = "INSERT INTO tracks (spotify_id, count, mood) VALUES {};".format(",".join(["("+",".join(["'" + str(k) + "'", str(v), "'" + mood + "'"])+")" for k,v in batch ]))
  cursor.execute(raw_sql)

def complete_features_from_db(mood, mysql):
  cursor = mysql.cursor()
  cursor.execute("SELECT spotify_id FROM tracks WHERE mood = '{}' AND popularity IS NULL".format(mood))
  tracks = cursor.fetchall()
  [retrieve_batch(tracks[i:i+BATCH_MAX_SIZE], mysql, mood, i, len(tracks)) for i in range(0, len(tracks), BATCH_MAX_SIZE)]

def retrieve_batch(ids, mysql, mood, idx, total_tracks_number):
  perc = idx * (BATCH_MAX_SIZE / total_tracks_number)
  print("%f" % perc)
  headers = {'Authorization': 'Bearer ' + access_token()["access_token"] }
  result_feat = requests.get(tracks_features_url([s_id[0] for s_id in ids]), headers = headers)
  result_std = requests.get(tracks_url([s_id[0] for s_id in ids]))
  if result_feat.status_code == 200 & result_std.status_code == 200:
    tracks_feat = result_feat.json()["audio_features"]
    tracks = result_std.json()["tracks"]
    combined_tracks = zip(tracks, tracks_feat)
    [write_features_to_db(track, mysql, mood) for track in combined_tracks]
    mysql.commit()

def write_features_to_db(track, mysql, mood):
  cursor = mysql.cursor()
  raw_sql = "UPDATE tracks SET title = '{}', artist = '{}', popularity = {}, duration_ms = {}, danceability = {}, acousticness = {}, energy = {}, liveness = {}, valence = {}, instrumentalness = {}, tempo = {}, speechiness = {}, loudness = {}, active = {} WHERE spotify_id = '{}'"
  if track[1] != None and track[0] != None:
    artist = re.sub('[^0-9a-zA-Z\s]+', '', track[0]["artists"][0]["name"])[:200] if (len(track[0]["artists"]) > 0) else "none"
    title = re.sub('[^0-9a-zA-Z\s]+', '', track[0]['name'])[:200] if (len(track[0]["name"])) else "none"
    values_list = (title, artist , track[0]["popularity"], (track[1]["duration_ms"] or 0), (track[1]["danceability"] or 0), (track[1]["acousticness"] or 0), (track[1]["energy"] or 0), (track[1]["liveness"] or 0), (track[1]["valence"] or 0), (track[1]["instrumentalness"] or 0), (track[1]["tempo"] or 0), (track[1]["speechiness"] or 0), (track[1]["loudness"] or 0), 1, track[0]['id'])
  else:
    values_list = ("null", "null" , -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, track[0]['id'])
  cursor.execute(raw_sql.format(*values_list))
