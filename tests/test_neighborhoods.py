import pytest
from src.problem import Depot, Customer, Vehicle, Route
from src.neighborhoods import apply_relocate, apply_swap, apply_2_opt

@pytest.fixture
def sample_data():
    depot = Depot(0, 0, 0)
    customers = [Customer(1, 1, 1, 10, 5), Customer(2, 2, 2, 5, 10), Customer(3, 3, 3, 8, 20)]
    vehicle = Vehicle(100, 300, 1.0)
    return depot, customers, vehicle

def test_apply_relocate_feasible(sample_data):
    depot, customers, vehicle = sample_data
    route1 = Route([depot, customers[0], depot])
    route2 = Route([depot, customers[1], depot])
    solution = [route1, route2]
    new_solution = apply_relocate(solution, vehicle)
    # Verificar se solução mudou ou não, mas sempre viável
    for r in new_solution:
        assert r.check_feasibility(vehicle)

def test_apply_swap_feasible(sample_data):
    depot, customers, vehicle = sample_data
    route1 = Route([depot, customers[0], depot])
    route2 = Route([depot, customers[1], depot])
    solution = [route1, route2]
    new_solution = apply_swap(solution, vehicle)
    for r in new_solution:
        assert r.check_feasibility(vehicle)

def test_apply_2_opt_feasible(sample_data):
    depot, customers, vehicle = sample_data
    route = Route([depot, customers[0], customers[1], depot])
    solution = [route]
    new_solution = apply_2_opt(solution, vehicle)
    for r in new_solution:
        assert r.check_feasibility(vehicle)

def test_apply_relocate_undo(sample_data):
    depot, customers, vehicle = sample_data
    # Criar veículo com capacity baixa para forçar inviabilidade
    low_capacity_vehicle = Vehicle(5, 300, 1.0)  # Capacity baixa
    route1 = Route([depot, customers[0], depot])  # Pickup 10
    route2 = Route([depot, customers[1], depot])  # Pickup 5
    original_solution = [route1, route2]
    # Copiar para comparar
    original_nodes = [r.nodes[:] for r in original_solution]
    # Aplicar relocate (deve falhar e reverter)
    result_solution = apply_relocate(original_solution, low_capacity_vehicle)
    # Verificar se voltou ao original
    for i, r in enumerate(result_solution):
        assert r.nodes == original_nodes[i]

def test_apply_swap_undo(sample_data):
    depot, customers, vehicle = sample_data
    low_capacity_vehicle = Vehicle(5, 300, 1.0)
    route1 = Route([depot, customers[0], depot])
    route2 = Route([depot, customers[1], depot])
    original_solution = [route1, route2]
    original_nodes = [r.nodes[:] for r in original_solution]
    result_solution = apply_swap(original_solution, low_capacity_vehicle)
    for i, r in enumerate(result_solution):
        assert r.nodes == original_nodes[i]