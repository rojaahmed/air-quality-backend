import osmnx as ox

place = "Gaziantep, Turkey"

print("Yollar indiriliyor...")

G = ox.graph_from_place(
    place,
    network_type="drive",
    simplify=True
)

ox.save_graphml(G, "gaziantep_roads.graphml")

print("Dosya kaydedildi!")