import random
from .problem import Route

def apply_relocate(solution, vehicle):
    if len(solution) < 2:
        return solution
    # Escolher rota origem e destino
    origin_idx = random.randint(0, len(solution) - 1)
    dest_idx = random.randint(0, len(solution) - 1)
    while dest_idx == origin_idx:
        dest_idx = random.randint(0, len(solution) - 1)
    origin_route = solution[origin_idx]
    dest_route = solution[dest_idx]
    # Escolher cliente na origem (não depot)
    customers = [i for i, n in enumerate(origin_route.nodes) if not isinstance(n, type(origin_route.nodes[0])) or n.id != 0]
    if not customers:
        return solution
    cust_idx = random.choice(customers)
    customer = origin_route.nodes[cust_idx]
    # Guardar posição original para undo
    origin_pos = cust_idx
    # Remover da origem
    origin_route.nodes.pop(cust_idx)
    # Inserir no destino (posição aleatória entre customers)
    dest_customers = [i for i, n in enumerate(dest_route.nodes) if not isinstance(n, type(dest_route.nodes[0])) or n.id != 0]
    if dest_customers:
        insert_pos = random.choice(dest_customers)
        dest_route.nodes.insert(insert_pos, customer)
    else:
        insert_pos = 1  # Após depot
        dest_route.nodes.insert(insert_pos, customer)
    # Verificar viabilidade
    if origin_route.check_feasibility(vehicle) and dest_route.check_feasibility(vehicle):
        return solution  # Aceitar mudança
    # Reverter: remover de dest e inserir de volta em origin
    dest_route.nodes.pop(insert_pos)
    origin_route.nodes.insert(origin_pos, customer)
    return solution

def apply_swap(solution, vehicle):
    if len(solution) < 2:
        return solution
    # Escolher duas rotas diferentes
    idx1 = random.randint(0, len(solution) - 1)
    idx2 = random.randint(0, len(solution) - 1)
    while idx2 == idx1:
        idx2 = random.randint(0, len(solution) - 1)
    route1 = solution[idx1]
    route2 = solution[idx2]
    # Escolher customers
    cust1 = [i for i, n in enumerate(route1.nodes) if not isinstance(n, type(route1.nodes[0])) or n.id != 0]
    cust2 = [i for i, n in enumerate(route2.nodes) if not isinstance(n, type(route2.nodes[0])) or n.id != 0]
    if not cust1 or not cust2:
        return solution
    pos1 = random.choice(cust1)
    pos2 = random.choice(cust2)
    # Guardar para undo
    cust1_orig = route1.nodes[pos1]
    cust2_orig = route2.nodes[pos2]
    # Swap
    route1.nodes[pos1], route2.nodes[pos2] = route2.nodes[pos2], route1.nodes[pos1]
    if route1.check_feasibility(vehicle) and route2.check_feasibility(vehicle):
        return solution  # Aceitar
    # Reverter swap
    route1.nodes[pos1], route2.nodes[pos2] = cust1_orig, cust2_orig
    return solution

def apply_2_opt(solution, vehicle):
    # Escolher uma rota
    if not solution:
        return solution
    route_idx = random.randint(0, len(solution) - 1)
    route = solution[route_idx]
    # Escolher dois pontos para 2-opt
    points = [i for i in range(1, len(route.nodes) - 1)]  # Não depot
    if len(points) < 2:
        return solution
    i, j = sorted(random.sample(points, 2))
    # Guardar segmento original para undo
    original_segment = route.nodes[i:j+1][:]
    # Reverter segmento
    route.nodes[i:j+1] = reversed(route.nodes[i:j+1])
    if route.check_feasibility(vehicle):
        return solution  # Aceitar
    # Reverter
    route.nodes[i:j+1] = original_segment
    return solution

def apply_relocate_station(solution, vehicle, stations):
    # Escolher uma rota que tenha estação
    for route in solution:
        station_indices = [i for i, n in enumerate(route.nodes) if isinstance(n, type(route.nodes[0])) and hasattr(n, 'id') and n.id >= 100]  # Assumindo IDs de estação >=100
        if station_indices:
            # Escolher estação e nova posição
            station_idx = random.choice(station_indices)
            station = route.nodes[station_idx]
            # Remover estação
            route.nodes.pop(station_idx)
            # Inserir em nova posição (não depot)
            possible_positions = [i for i in range(1, len(route.nodes))]  # Não início/fim
            if possible_positions:
                new_pos = random.choice(possible_positions)
                route.nodes.insert(new_pos, station)
                if route.check_feasibility(vehicle):
                    return solution  # Aceitar
                # Reverter
                route.nodes.pop(new_pos)
                route.nodes.insert(station_idx, station)
    return solution

def apply_swap_station(solution, vehicle, stations):
    # Escolher rota com estação
    for route in solution:
        station_indices = [i for i, n in enumerate(route.nodes) if isinstance(n, type(route.nodes[0])) and hasattr(n, 'id') and n.id >= 100]
        if station_indices and stations:
            station_idx = random.choice(station_indices)
            current_station = route.nodes[station_idx]
            # Escolher nova estação diferente
            new_stations = [s for s in stations if s.id != current_station.id]
            if new_stations:
                new_station = random.choice(new_stations)
                route.nodes[station_idx] = new_station
                if route.check_feasibility(vehicle):
                    return solution  # Aceitar
                # Reverter
                route.nodes[station_idx] = current_station
    return solution

def apply_exchange(solution, vehicle):
    # Placeholder
    return solution