import networkx as nx
import os
import time
from statistics import mean, median
from collections import Counter

# Prompt the user to choose a graph in the ./graphs directory. Then read and return that graph as a networkx graph object.
def read_graph():
    graph_directory="./graphs"
    file_list = [f for f in os.listdir(graph_directory) if os.path.isfile(os.path.join(graph_directory, f))]
    file_chosen=None
    print("Which file to read(enter a number):")
    while(True):
        ctr=1
        for f in file_list:
            print(ctr,":",f)
            ctr+=1
        choice=input()
        if(choice.isnumeric() and int(choice)<=len(file_list) and int(choice)>0):
            file_chosen=file_list[int(choice)-1]
            break
        else: print("Try again:")
    graph_path=os.path.join(graph_directory,file_chosen)
    print("Reading network...")
    G=nx.read_gml(graph_path)
    print("Network is built!")
    return G

# Analyze the graph and print out the results
def analyze_graph(G):
    # Start the clock
    start_time = time.time()
    # Calculate Statistics
    # Total nodes & edges
    total_nodes = G.number_of_nodes()
    total_edges = G.number_of_edges()
    print(f"Total number of nodes: {total_nodes}")
    print(f"Total number of edges: {total_edges}")

    # Playlist & Track nodes
    playlist_nodes = [n for n, d in G.nodes(data=True) if d['type'] == 'playlist']
    track_nodes = [n for n, d in G.nodes(data=True) if d['type'] == 'track']
    print(f"Number of playlist nodes: {len(playlist_nodes)}")
    print(f"Number of track nodes: {len(track_nodes)}")

    # Degrees (all nodes, playlist nodes, track nodes)
    all_degrees = [deg for node, deg in G.degree()]
    playlist_degrees = [deg for node, deg in G.degree(playlist_nodes)]
    track_degrees = [deg for node, deg in G.degree(track_nodes)]

    # Function to calculate mode(s)
    def get_modes(data):
        count = Counter(data)
        max_count = max(count.values())
        modes = [item for item, count in count.items() if count == max_count]
        return modes

    for degrees, label in zip([all_degrees, playlist_degrees, track_degrees], ["all", "playlist", "track"]):
        print(f"\nDegrees for {label} nodes:")
        print(f"Min Degree: {min(degrees)}")
        print(f"Max Degree: {max(degrees)}")
        print(f"Mean Degree: {mean(degrees):.4f}")
        print(f"Median Degree: {median(degrees)}")
        modes = get_modes(degrees)
        if len(modes) > 1:
            print(f"Modes Degree: {', '.join(map(str, modes))}")
        else:
            print(f"Mode Degree: {modes[0]}")



    # Extract nodes with highest degrees for playlist and track
    sorted_playlist_nodes = sorted(playlist_nodes, key=G.degree, reverse=True)[:5]
    sorted_track_nodes = sorted(track_nodes, key=G.degree, reverse=True)[:5]

    print("Top 5 Playlists by Degree:")
    for node in sorted_playlist_nodes:
        print(f"Playlist: {G.nodes[node]['name']}, Degree: {G.degree[node]}")

    print("\nTop 5 Tracks by Degree:")
    for node in sorted_track_nodes:
        print(f"Track: {G.nodes[node]['track_name']} by {G.nodes[node]['artist_name']}, Degree: {G.degree[node]}")



    # Average & Global Clustering Coefficients
    avg_clustering_all = nx.average_clustering(G)
    avg_clustering_playlist = nx.average_clustering(G.subgraph(playlist_nodes))
    avg_clustering_track = nx.average_clustering(G.subgraph(track_nodes))

    print(f"\nAverage clustering coefficient (all nodes): {avg_clustering_all:.4f}")
    print(f"Average clustering coefficient (playlist nodes): {avg_clustering_playlist:.4f}")
    print(f"Average clustering coefficient (track nodes): {avg_clustering_track:.4f}")

    global_clustering_all = nx.transitivity(G)
    global_clustering_playlist = nx.transitivity(G.subgraph(playlist_nodes))
    global_clustering_track = nx.transitivity(G.subgraph(track_nodes))

    print(f"\nGlobal clustering coefficient (all nodes): {global_clustering_all:.4f}")
    print(f"Global clustering coefficient (playlist nodes): {global_clustering_playlist:.4f}")
    print(f"Global clustering coefficient (track nodes): {global_clustering_track:.4f}")

    # Connected components (for undirected graph)
    connected_comp = list(nx.connected_components(G))

    print(f"\nNumber of connected components: {len(connected_comp)}")
    print(f"Size of largest connected component: {len(max(connected_comp, key=len))}")

    # End the clock and print the runtime
    end_time = time.time()
    print(f"\nRuntime: {end_time - start_time:.2f} seconds")
