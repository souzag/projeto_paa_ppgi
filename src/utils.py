import json
import math
from .problem import Depot, Customer, ChargingStation, Vehicle, Route

def calculate_distance(node1, node2):
    return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

def load_problem_data(filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"Arquivo {filepath} não encontrado.")
    except json.JSONDecodeError:
        raise ValueError(f"Erro ao decodificar JSON em {filepath}.")

    # Validação de depot
    depot_data = data.get('depot')
    if not depot_data or not all(k in depot_data for k in ['id', 'x', 'y']):
        raise ValueError("Dados do depot incompletos.")
    if not isinstance(depot_data['id'], int) or not all(isinstance(v, (int, float)) for v in [depot_data['x'], depot_data['y']]):
        raise ValueError("Depot: id deve ser int, x/y devem ser numéricos.")

    # Validação de customers
    customers_data = data.get('customers', [])
    if not isinstance(customers_data, list):
        raise ValueError("Customers deve ser uma lista.")
    ids = set()
    for c in customers_data:
        if not all(k in c for k in ['id', 'x', 'y', 'pickup', 'delivery']):
            raise ValueError("Customer com dados incompletos.")
        if not isinstance(c['id'], int) or c['id'] in ids:
            raise ValueError("Customer id deve ser int único.")
        if not all(isinstance(v, (int, float)) for v in [c['x'], c['y'], c['pickup'], c['delivery']]):
            raise ValueError("Customer: x/y/pickup/delivery devem ser numéricos.")
        if c['pickup'] < 0 or c['delivery'] < 0:
            raise ValueError("Pickup e delivery devem ser não-negativos.")
        ids.add(c['id'])

    # Validação de charging_stations
    stations_data = data.get('charging_stations', [])
    if not isinstance(stations_data, list):
        raise ValueError("Charging_stations deve ser uma lista.")
    for cs in stations_data:
        if not all(k in cs for k in ['id', 'x', 'y']):
            raise ValueError("ChargingStation com dados incompletos.")
        if not isinstance(cs['id'], int) or cs['id'] in ids:
            raise ValueError("ChargingStation id deve ser int único.")
        if not all(isinstance(v, (int, float)) for v in [cs['x'], cs['y']]):
            raise ValueError("ChargingStation: x/y devem ser numéricos.")
        ids.add(cs['id'])

    # Validação de vehicle
    vehicle_data = data.get('vehicle')
    if not vehicle_data or not all(k in vehicle_data for k in ['capacity', 'battery', 'consumption_rate']):
        raise ValueError("Dados do vehicle incompletos.")
    if not all(isinstance(v, (int, float)) and v > 0 for v in [vehicle_data['capacity'], vehicle_data['battery'], vehicle_data['consumption_rate']]):
        raise ValueError("Vehicle: capacity, battery, consumption_rate devem ser numéricos positivos.")

    depot = Depot(depot_data['id'], depot_data['x'], depot_data['y'])
    customers = [Customer(c['id'], c['x'], c['y'], c['pickup'], c['delivery']) for c in customers_data]
    charging_stations = [ChargingStation(cs['id'], cs['x'], cs['y']) for cs in stations_data]
    vehicle = Vehicle(vehicle_data['capacity'], vehicle_data['battery'], vehicle_data['consumption_rate'])
    return depot, customers, charging_stations, vehicle

def calculate_total_cost(solution):
    return sum(route.calculate_cost() for route in solution)

def generate_random_instance(num_customers=50, num_stations=5, seed=None):
    import random
    if seed:
        random.seed(seed)
    # Depot fixo
    depot = {"id": 0, "x": 50, "y": 50}
    # Clientes aleatórios
    customers = []
    for i in range(1, num_customers + 1):
        customers.append({
            "id": i,
            "x": random.uniform(0, 100),
            "y": random.uniform(0, 100),
            "pickup": random.uniform(5, 20),
            "delivery": random.uniform(5, 20)
        })
    # Estações aleatórias
    stations = []
    for i in range(101, 101 + num_stations):
        stations.append({
            "id": i,
            "x": random.uniform(0, 100),
            "y": random.uniform(0, 100)
        })
    # Veículo com parâmetros variados
    vehicle = {
        "capacity": random.uniform(50, 150),
        "battery": random.uniform(200, 500),
        "consumption_rate": random.uniform(0.5, 2.0)
    }
    return {
        "depot": depot,
        "customers": customers,
        "charging_stations": stations,
        "vehicle": vehicle
    }

def evaluate_solution(solution):
    total_cost = calculate_total_cost(solution)
    num_routes = len(solution)
    # Diversidade: média da distância entre centros das rotas
    if num_routes > 1:
        centers = []
        for route in solution:
            x_avg = sum(n.x for n in route.nodes) / len(route.nodes)
            y_avg = sum(n.y for n in route.nodes) / len(route.nodes)
            centers.append((x_avg, y_avg))
        diversity = sum(math.sqrt((centers[i][0] - centers[j][0])**2 + (centers[i][1] - centers[j][1])**2)
                        for i in range(num_routes) for j in range(i+1, num_routes)) / (num_routes * (num_routes - 1) / 2)
    else:
        diversity = 0
    return {
        'total_cost': total_cost,
        'num_routes': num_routes,
        'diversity': diversity
    }

def find_nearest_station(route, stations, vehicle):
    # Tentar inserir estação para tornar rota viável
    # Simples: para cada posição possível, testar inserir cada estação e ver se viável com menor custo adicional
    min_cost = float('inf')
    best_route = None
    for i in range(1, len(route.nodes)):  # Não no início/fim
        for station in stations:
            new_nodes = route.nodes[:i] + [station] + route.nodes[i:]
            new_route = Route(new_nodes)
            if new_route.check_feasibility(vehicle):
                cost = new_route.calculate_cost() - route.calculate_cost()
                if cost < min_cost:
                    min_cost = cost
                    best_route = new_route
    return best_route if best_route else None