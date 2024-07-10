# Music-Recommendation-Prediction

Project Setup: (Python 3.7 or above)

Download the dataset from https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge/dataset_files
Unzip the dataset and place the "spotify_million_playlist_dataset" in the root directory
Run generate_network.py to generate graphs. All .gml files generated are placed in graphs/. Other .gml files need to be in graphs/ as well for read_graph() to be able to detect.
(Optional) Call analyze_graph in herlpers.py to analyze graphs.
Set input playlist in recommender.py following the format of [song_name-artist_name](note that the songs have to be present in the dataset). https://github.com/zechengF2023/Network-Project-T19/blob/39f120ae8dc97b975ae6308a09f07a0f5dc4d5d0/recommender.py#L8C1-L9C1
Run recommender.py to recommend songs.
