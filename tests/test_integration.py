import pytest
from src.utils import load_problem_data, calculate_total_cost
from src.initial_solution import modified_clarke_wright_savings
from src.vns import run_vns

def test_full_flow():
    depot, customers, charging_stations, vehicle = load_problem_data('data/instancia_teste.json')
    initial_routes = modified_clarke_wright_savings(customers, vehicle, depot, charging_stations)
    initial_cost = calculate_total_cost(initial_routes)
    final_solution, _ = run_vns(initial_routes, k_max=3, max_iter=10, vehicle=vehicle)  # Menos iterações para teste
    final_cost = calculate_total_cost(final_solution)
    assert final_cost <= initial_cost
    for route in final_solution:
        assert route.check_feasibility(vehicle)