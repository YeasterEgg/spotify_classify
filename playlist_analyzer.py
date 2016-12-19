import pandas as pd
import os
import MySQLdb

## PARSING METHODS

def analyze_playlist(mysql, playlist):
  tracks = []
  cursor = mysql.cursor(MySQLdb.cursors.DictCursor)
  for key, value in playlist["songlist"].items():
    parsed_track = parse_track(playlist, value)
    cursor.execute("SELECT * FROM tracks WHERE spotify_id = '{}' AND training = {}".format(value["spotifyId"], playlist["training"]))
    if cursor:
      parsed_track = cursor.fetchone()
    else:
      parsed_track = parse_track(playlist, value)
      track_to_db(mysql, parsed_track)
    tracks.append(parsed_track)
  return tracks

def parse_track(playlist, track):
  parsed = {}
  parsed["spotify_id"]       = track["spotifyId"]
  parsed["mood"]             = playlist["mood"]
  parsed["training"]         = playlist["training"]
  parsed["duration_ms"]      = track["duration_ms"]
  parsed["danceability"]     = track["features"]["danceability"]
  parsed["acousticness"]     = track["features"]["acousticness"]
  parsed["energy"]           = track["features"]["energy"]
  parsed["liveness"]         = track["features"]["liveness"]
  parsed["valence"]          = track["features"]["valence"]
  parsed["instrumentalness"] = track["features"]["instrumentalness"]
  parsed["tempo"]            = track["features"]["tempo"]
  parsed["speechiness"]      = track["features"]["speechiness"]
  parsed["loudness"]         = track["features"]["loudness"]
  parsed["count"]            = 0
  return parsed

## STORING METHODS

def track_to_db(mysql, track):
  mysql.cursor.execute("""INSERT INTO tracks (spotify_id, mood, duration_ms, danceability, acousticness, energy, liveness, valence, instrumentalness, tempo, speechiness, loudness, training, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, NOW())""",(track["spotify_id"], track["mood"], track["duration_ms"], track["danceability"], track["acousticness"], track["energy"], track["liveness"], track["valence"], track["instrumentalness"], track["tempo"], track["speechiness"], track["loudness"], track["training"]))
  mysql.commit()

## ANALYSIS METHODS

def assign_playlist(playlist):
  results = {}
  for track in playlist:
    print(track)
    results["spotify_id"] = track["spotify_id"]
  return results

