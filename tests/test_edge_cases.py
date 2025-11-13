import pytest
from src.problem import Depot, Customer, Vehicle, Route
from src.initial_solution import modified_clarke_wright_savings

def test_small_instance():
    depot = Depot(0, 0, 0)
    customers = [Customer(1, 1, 1, 10, 5)]
    vehicle = Vehicle(100, 300, 1.0)
    routes = modified_clarke_wright_savings(customers, vehicle, depot)
    assert len(routes) == 1
    assert routes[0].check_feasibility(vehicle)

def test_no_feasible_solution():
    depot = Depot(0, 0, 0)
    customers = [Customer(1, 100, 100, 10, 5)]  # Longe, bateria insuficiente
    vehicle = Vehicle(100, 10, 1.0)  # Bateria baixa
    routes = modified_clarke_wright_savings(customers, vehicle, depot)
    # Pode não ser viável, mas algoritmo tenta
    # Apenas verificar que não quebra
    assert isinstance(routes, list)