# Spotify Mood

A simple python API app based on ~~Flask~~ ~~Sanic~~ Hug that classifies tracklists using Linear Discriminant Analysis or a better model (ASAP will be using neural networks).
Uses Pandas and Scikit-Learn to organize and analyze data.

## How does it works

Starts with
```hug -f main.py```

#### Classification Models

Each classification model is binary, as in it can classify only between 2 moods.
The models I've created used other users' playlists from spotify defined by some mood, as *happy* or *sad*.
The dataset is retrieved from spotify, then all songs that are in both the classes are removed from the model, and are weighted against number of occurences / popularity.

#### Moods Classification

The POST endpoint **/{version}/playlist** (authenticated via a SHA256 digested shared token with the main application) receives a JSON containing a tracklist with the data retrieved by the Spotify API. Then it checks the song against an LDA model previously created and saved. The response is a JSON with each track expressed as a key/value pair with spotify_id/classification.

#### Moods

In this particular case, I've created it in order to classify the "mood" of a track.

#### Songs

The GET endpoint /songs?{limit} allows to receive the data retrieved from Spotify for {limit} songs (or all of them).

## TODOs

- Neural Networks
