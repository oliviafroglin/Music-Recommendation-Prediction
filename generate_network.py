import networkx as nx
import json
import time

# Prompt the user for the number of files to process
try:
    num_files = int(input("Enter the number of files to process (up to 1000): "))
    if not (1 <= num_files <= 1000):
        print("Please enter a number between 1 and 1000.")
        exit()
except ValueError:
    print("Please enter a valid integer!")
    exit()

# Start the clock
start_time = time.time()

# Generate filenames based on user input
files_to_process = [f'./spotify_million_playlist_dataset/data/mpd.slice.{i*1000}-{(i+1)*1000-1}.json' for i in range(num_files)]

# Initialize variables
playlists = []

# Load data from all files
for filename in files_to_process:
    with open(filename, 'r') as file:
        data = json.load(file)
        playlists.extend(data['playlists'])

# Determine min and max followers across all loaded playlists
min_followers = float('inf')
max_followers = float('-inf')

for playlist in playlists:
    followers = playlist['num_followers']
    min_followers = min(min_followers, followers)
    max_followers = max(max_followers, followers)

# Function to normalize followers using Min-Max scaling with a small offset
def normalize_followers(followers):
    return (followers - min_followers + 1) / (max_followers - min_followers + 1)

# Initialize a graph
G = nx.Graph()

# Build the graph using the loaded playlists
for playlist in playlists:
    pid = playlist['pid']
    playlist_name = playlist['name']
    playlist_followers = playlist['num_followers']
    
    # Add playlist node
    G.add_node(pid, type="playlist", name=playlist_name, num_followers=playlist_followers)
    
    for track in playlist['tracks']:
        # Using track_name + artist_name as unique identifier for the track
        track_id = track['track_name'] + "-" + track['artist_name']
        
        # Add track node if not already in the graph
        if track_id not in G:
            G.add_node(track_id, type="track", track_name=track['track_name'], artist_name=track['artist_name'], album_name=track['album_name'])
        
        # Connect playlist to its track
        G.add_edge(pid, track_id, weight=normalize_followers(playlist_followers))

# Save the network to a file
filename = f"./graphs/playlist_network_{num_files}-files.gml"
nx.write_gml(G, filename)
print(f"Graph saved to {filename}")
end_time = time.time()
print(f"Runtime: {end_time - start_time:.2f} seconds")

