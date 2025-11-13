import time
from src.utils import load_problem_data, calculate_total_cost
from src.initial_solution import modified_clarke_wright_savings
from src.vns import run_vns

def test_performance():
    depot, customers, charging_stations, vehicle = load_problem_data('data/instancia_teste.json')
    start = time.time()
    initial_routes = modified_clarke_wright_savings(customers, vehicle, depot, charging_stations)
    initial_time = time.time() - start
    initial_cost = calculate_total_cost(initial_routes)
    initial_routes_count = len(initial_routes)

    start = time.time()
    final_solution = run_vns(initial_routes, k_max=3, max_iter=50, vehicle=vehicle)
    vns_time = time.time() - start
    final_cost = calculate_total_cost(final_solution)
    final_routes_count = len(final_solution)

    print(f"Tempo inicial: {initial_time:.4f}s, Custo: {initial_cost:.2f}, Rotas: {initial_routes_count}")
    print(f"Tempo VNS: {vns_time:.4f}s, Custo: {final_cost:.2f}, Rotas: {final_routes_count}")
    assert final_cost <= initial_cost
    assert vns_time > 0  # Apenas verificar que executou