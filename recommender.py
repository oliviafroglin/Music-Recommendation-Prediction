import helpers
import collections
import random

# The recommender algorithm

# Input format: [song_name-artist_name].
input_playlist=["Toxic-Britney Spears", "Lose Control (feat. Ciara & Fat Man Scoop)-Missy Elliott", "Crazy In Love-Beyonc\u00e9"]
NUM_TO_RECOMMEND=10
input_playlist=set(input_playlist)

# Read graph
G=helpers.read_graph()

# Compute weights between neighboring playlists and input playlist
playlist_to_weight=collections.defaultdict(int)
for input_song in input_playlist:
    for neighbor_playlist in G.neighbors(input_song):
        playlist_to_weight[neighbor_playlist]+=G.edges[input_song,neighbor_playlist]["weight"]

# Compute weights between songs of neighboring playlists (excluding input songs) and the input playlist
song_to_weight=collections.defaultdict(int)
for p in playlist_to_weight.keys():
    for song in G.neighbors(p):
        if(song not in input_playlist):
            song_to_weight[song]=G.edges[p,song]["weight"]+playlist_to_weight[p]

# Choose songs to recommend based on their weights
songs_to_recommend = []
while len(songs_to_recommend) < NUM_TO_RECOMMEND and len(song_to_weight) > 0:
    chosen_song = random.choices(population=[song for song, _ in song_to_weight.items()], weights=[prob for _, prob in song_to_weight.items()])[0]
    if chosen_song not in songs_to_recommend:
        del song_to_weight[chosen_song]
        songs_to_recommend.append(chosen_song)

print(songs_to_recommend)

