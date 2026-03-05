import osmnx as ox

# graph dosyasını yükle
G = ox.load_graphml("gaziantep_roads.graphml")

# kaç node ve edge var
print("Node sayısı:", len(G.nodes))
print("Edge sayısı:", len(G.edges))