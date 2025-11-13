from .utils import calculate_distance, find_nearest_station
from .problem import Route

def modified_clarke_wright_savings(customers, vehicle, depot, stations=None):
    if stations is None:
        stations = []
    # Inicializar rotas: cada cliente em sua própria rota
    routes = [Route([depot, c, depot]) for c in customers]

    # Calcular savings
    savings = []
    for i in range(len(customers)):
        for j in range(i + 1, len(customers)):
            s = (calculate_distance(depot, customers[i]) +
                 calculate_distance(depot, customers[j]) -
                 calculate_distance(customers[i], customers[j]))
            savings.append((s, i, j))

    # Ordenar savings decrescente
    savings.sort(reverse=True, key=lambda x: x[0])

    # Para cada saving, tentar fundir rotas
    for s, i, j in savings:
        route_i = None
        route_j = None
        for r in routes:
            if customers[i] in r.nodes:
                route_i = r
            if customers[j] in r.nodes:
                route_j = r

        if route_i == route_j or route_i is None or route_j is None:
            continue

        # Tentar fundir: nova rota combinando
        # Assumir fusão simples: route_i.nodes[:-1] + route_j.nodes[1:]
        new_nodes = route_i.nodes[:-1] + route_j.nodes[1:]
        new_route = Route(new_nodes)

        if new_route.check_feasibility(vehicle):
            routes.remove(route_i)
            routes.remove(route_j)
            routes.append(new_route)
        else:
            # Tentar inserir estação para tornar viável
            improved_route = find_nearest_station(new_route, stations, vehicle)
            if improved_route:
                routes.remove(route_i)
                routes.remove(route_j)
                routes.append(improved_route)

    return routes

def generate_nearest_neighbor_solution(customers, vehicle, depot, stations=None):
    if stations is None:
        stations = []
    routes = []
    unvisited = set(customers)
    while unvisited:
        route = [depot]
        current_load = 0
        current_battery = vehicle.battery
        current_node = depot
        while unvisited:
            # Encontrar cliente mais próximo não visitado
            nearest = None
            min_dist = float('inf')
            for c in unvisited:
                dist = calculate_distance(current_node, c)
                if dist < min_dist:
                    min_dist = dist
                    nearest = c
            if nearest is None:
                break
            # Verificar se pode adicionar
            temp_load = current_load + nearest.pickup
            temp_battery = current_battery - min_dist * vehicle.consumption_rate
            if temp_load > vehicle.capacity or temp_battery < 0:
                break
            # Adicionar
            route.append(nearest)
            current_load = temp_load - nearest.delivery
            if current_load < 0:
                current_load = 0
            current_battery = temp_battery
            current_node = nearest
            unvisited.remove(nearest)
        route.append(depot)
        routes.append(Route(route))
    return routes