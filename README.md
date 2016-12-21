# Spotify Mood

A simple python API app based on Flask that classifies tracklists using Linear Discriminant Analysis.
Uses Pandas and Scikit-Learn to organize and analyze data.


## How does it works

The first part is the creation of the classification model: since it stores the tracklists it receives, if a track has already a mood when it's received, and it has the flag *training*, can be selected to create a classification model.

#### Classification Models

Each classification model is binary, as in it can classify only between 2 moods. The GET endpoint **/{version}/reload_params?moods={mood1_mood2}&token={SECRET}** recreates the model using the tracks in the database.
The models I've created used other users' playlists from spotify defined by some mood, as *happy* or *sad*.

#### Moods Classification

The POST endpoint **/{version}/playlist** (authenticated via a SHA256 digested shared token with the main application) receives a JSON containing a tracklist with the data retrieved by the Spotify API. Then it checks the song against an LDA model previously created and saved. The response is a JSON with each track expressed as a key/value pair with spotify_id/classification.


#### Moods

In this particular case, I've created it in order to classify the "mood" of a track.


## TODOs

- When a track is classified, it's mood should be added to the db, so that will be retrieved from it instead of being reclassified
- Many many other things
