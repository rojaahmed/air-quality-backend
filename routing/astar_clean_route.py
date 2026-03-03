import heapq
from utils.geo_utils import haversine
from utils.traffic_utils import traffic_multiplier
from services.clean_route_service import idw_aqi


def heuristic(lat1, lon1, lat2, lon2):
    return haversine(lat1, lon1, lat2, lon2)


def clean_cost(prev_node, next_node):
    lat1, lon1 = prev_node
    lat2, lon2 = next_node

    dist = haversine(lat1, lon1, lat2, lon2)
    aqi = idw_aqi(lat2, lon2)
    traffic = traffic_multiplier()

    return dist + (aqi * 3) + (traffic * 10)


def astar_clean_route(G, start_node, end_node):
    pq = []
    heapq.heappush(pq, (0, start_node))
    
    came_from = {start_node: None}
    cost_so_far = {start_node: 0}

    while pq:
        _, current = heapq.heappop(pq)

        if current == end_node:
            break

        for neighbor in G.neighbors(current):
            lat1 = G.nodes[current]["y"]
            lon1 = G.nodes[current]["x"]
            lat2 = G.nodes[neighbor]["y"]
            lon2 = G.nodes[neighbor]["x"]

            new_cost = cost_so_far[current] + clean_cost((lat1, lon1), (lat2, lon2))

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost

                h = heuristic(lat2, lon2, 
                              G.nodes[end_node]["y"],
                              G.nodes[end_node]["x"])

                heapq.heappush(pq, (new_cost + h, neighbor))
                came_from[neighbor] = current

    route = []
    node = end_node
    while node:
        route.append(node)
        node = came_from[node]

    return list(reversed(route))