import osmnx as ox
import pickle

place = "Gaziantep, Turkey"

# yol grafiğini indir
G = ox.graph_from_place(place, network_type="drive")

# edge verilerini temizle
for u, v, k, data in G.edges(keys=True, data=True):
    data.clear()

# node verilerinden sadece koordinat bırak
for node, data in G.nodes(data=True):
    lat = data["y"]
    lon = data["x"]
    data.clear()
    data["y"] = lat
    data["x"] = lon

# kaydet
with open("roads.pkl","wb") as f:
    pickle.dump(G,f)

print("Optimize graph kaydedildi")