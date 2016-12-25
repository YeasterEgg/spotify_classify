import os
import requests
import base64
import csv
from os.path import join, dirname
from dotenv import load_dotenv

current_path = dirname(__file__)
dotenv_path = join(current_path, '.env')
load_dotenv(dotenv_path)

def token_url():
  return "https://accounts.spotify.com/api/token"

def search_url(query, obj_type = "playlist", limit = 50, offset = 0):
  return "https://api.spotify.com/v1/search?q={}&type={}&limit={}&offset={}".format(query, obj_type, limit, offset)

def playlist_url(user_id, playlist_id):
  return "https://api.spotify.com/v1/users/{}/playlists/{}/tracks".format(user_id, playlist_id)

def track_features_url(song_id):
  return "https://api.spotify.com/v1/audio-features/{}".format(song_id)

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
    with open("{}/lists/{}.txt".format(current_path, mood), "w") as file:
      for playlist in result.json()["playlists"]["items"]:
        file.write(playlist["tracks"]["href"])
        file.write("\n")
    if next_url is not None:
      recover_playlist_from_query(mood, next_url, counter = counter + 1)
  return "{}/lists/{}.txt".format(current_path, mood)

def recover_tracks_from_playlists(playlists_filename):
  playlists_no = count_lines(playlists_filename)
  headers = {'Authorization': 'Bearer ' + access_token()["access_token"] }
  tracks_filename = "tracks_{}".format(playlists_filename)
  counter = 0
  with open("{}/lists/{}".format(current_path, playlists_filename), "r") as playlists:
    with open("{}/lists/{}".format(current_path, tracks_filename), "w") as tracks:
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

def recover_features_from_tracks(mood, mysql):
  tracks_file = "{}/lists/{}".format(current_path, mood)
  tracks_no = count_lines(tracks_file)
  counter = 0
  with open(tracks_file, "r") as file:
    for track_id in file:
      print("{}%".format((counter * 100) / tracks_no))
      counter = counter + 1
      clean_id = track_id.strip("\n")
      write_features_to_db(clean_id, mysql, mood)

def write_features_to_db(track_id, mysql, mood):
  headers = {'Authorization': 'Bearer ' + access_token()["access_token"] }
  cursor = mysql.cursor()
  cursor.execute("SELECT COUNT(*) from tracks WHERE spotify_id = '{}'".format(track_id))
  count = cursor.fetchone()
  if count[0] == 0:
    result = requests.get(track_features_url(track_id), headers = headers)
    if result.status_code == 200:
      track = result.json()
      cursor.execute("INSERT INTO tracks (mood, spotify_id, duration_ms, danceability, acousticness, energy, liveness, valence, instrumentalness, tempo, speechiness, loudness, count) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{})".format(mood, track_id, (track["duration_ms"] or 0), (track["danceability"] or 0), (track["acousticness"] or 0), (track["energy"] or 0), (track["liveness"] or 0), (track["valence"] or 0), (track["instrumentalness"] or 0), (track["tempo"] or 0), (track["speechiness"] or 0), (track["loudness"] or 0), 1))
  else:
    cursor.execute("UPDATE tracks SET count = count + 1 WHERE spotify_id = '{}';".format(track_id))
  mysql.commit()

