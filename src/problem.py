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
            # 1. Carga Inicial: Soma de todas as entregas na rota
            current_load = sum(node.delivery for node in self.nodes if isinstance(node, Customer))
            if current_load > vehicle.capacity:
                return False  # Rota inviável desde o início

            current_battery = vehicle.battery
            last_node = self.nodes[0]  # Começa no depósito

            for i in range(1, len(self.nodes)):
                node = self.nodes[i]

                # 2. Consumo de Bateria
                distance = self.calculate_distance(last_node, node)
                current_battery -= distance * vehicle.consumption_rate

                if current_battery < 0:
                    return False  # Sem bateria para chegar ao nó

                # 3. Lógica no Nó
                if isinstance(node, Customer):
                    # 3a. Entrega Primeiro
                    current_load -= node.delivery

                    # 3b. Coleta Depois
                    current_load += node.pickup

                    # 3c. Verifica Capacidade APÓS a coleta
                    if current_load > vehicle.capacity:
                        return False

                elif isinstance(node, ChargingStation):
                    # 3d. Recarrega
                    current_battery = vehicle.battery

                last_node = node

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