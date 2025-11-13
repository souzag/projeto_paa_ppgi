import math

class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Customer(Node):
    def __init__(self, id, x, y, pickup, delivery):
        super().__init__(id, x, y)
        self.pickup = pickup
        self.delivery = delivery

class Depot(Node):
    def __init__(self, id, x, y):
        super().__init__(id, x, y)

class ChargingStation(Node):
    def __init__(self, id, x, y):
        super().__init__(id, x, y)

class Vehicle:
    def __init__(self, capacity, battery, consumption_rate):
        self.capacity = capacity
        self.battery = battery
        self.consumption_rate = consumption_rate

class Route:
    def __init__(self, nodes):
        self.nodes = nodes  # Lista de Node, começando e terminando com Depot

    def calculate_distance(self, node1, node2):
        return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

    def check_feasibility(self, vehicle):
        try:
            # Verificar capacidade e bateria
            current_load = 0
            current_battery = vehicle.battery
            for i in range(len(self.nodes) - 1):
                node = self.nodes[i]
                next_node = self.nodes[i + 1]
                distance = self.calculate_distance(node, next_node)
                # Atualizar carga se for Customer
                if isinstance(node, Customer):
                    current_load += node.pickup
                    if current_load > vehicle.capacity:
                        return False
                    current_load -= node.delivery
                    if current_load < 0:
                        current_load = 0
                # Consumir bateria
                current_battery -= distance * vehicle.consumption_rate
                if current_battery < 0:
                    return False
                # Se for ChargingStation, recarregar bateria
                if isinstance(next_node, ChargingStation):
                    current_battery = vehicle.battery  # Assumir recarga completa
            return True
        except (TypeError, ValueError, AttributeError) as e:
            print(f"Erro em check_feasibility: {e}")
            return False

    def calculate_cost(self):
        try:
            cost = 0
            for i in range(len(self.nodes) - 1):
                cost += self.calculate_distance(self.nodes[i], self.nodes[i + 1])
            return cost
        except (TypeError, ValueError, AttributeError) as e:
            print(f"Erro em calculate_cost: {e}")
            return float('inf')  # Retornar infinito para indicar erro