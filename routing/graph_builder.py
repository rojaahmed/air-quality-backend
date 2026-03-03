import osmnx as ox
import networkx as nx

def load_graph():
    print("🌍 Gaziantep yol ağı yükleniyor...")
    G = ox.graph_from_place("Gaziantep, Turkey", network_type="drive")
    G = ox.add_edge_lengths(G)  
    return G