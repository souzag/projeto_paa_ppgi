from src.utils import load_problem_data, calculate_total_cost, generate_random_instance
from src.initial_solution import modified_clarke_wright_savings, generate_nearest_neighbor_solution
from src.vns import run_vns
from src.visualization import plot_convergence
import matplotlib.pyplot as plt
import statistics
import time
import json
import sys

if __name__ == "__main__":
    # Argumentos: num_customers, num_stations, seed
    num_customers = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    num_stations = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 42

    # Gerar instância
    instance_data = generate_random_instance(num_customers=num_customers, num_stations=num_stations, seed=seed)
    instance_file = f'data/instance_{num_customers}_{num_stations}_{seed}.json'
    with open(instance_file, 'w') as f:
        json.dump(instance_data, f, indent=2)
    depot, customers, charging_stations, vehicle = load_problem_data(instance_file)
    print(f"Instância gerada: {len(customers)} clientes, {len(charging_stations)} estações, Seed {seed}")
    print(f"Veículo: Capacidade {vehicle.capacity:.1f}, Bateria {vehicle.battery:.1f}, Consumo {vehicle.consumption_rate:.1f}")

    # Log de métricas
    log = []

    # Nearest Neighbor
    start = time.time()
    nn_solution = generate_nearest_neighbor_solution(customers, vehicle, depot, charging_stations)
    nn_time = time.time() - start
    nn_cost = calculate_total_cost(nn_solution)
    log.append({"method": "NN", "cost": nn_cost, "time": nn_time, "routes": len(nn_solution)})
    print("Solução NN:")
    print(f"Custo NN: {nn_cost:.2f}, Tempo: {nn_time:.4f}s, Rotas: {len(nn_solution)}")

    # VNS pós-NN
    start = time.time()
    vns_nn, _ = run_vns(nn_solution, k_max=3, max_iter=50, vehicle=vehicle, stations=charging_stations)
    vns_nn_time = time.time() - start
    vns_nn_cost = calculate_total_cost(vns_nn)
    log.append({"method": "VNS pos-NN", "cost": vns_nn_cost, "time": vns_nn_time, "routes": len(vns_nn)})
    print(f"VNS pós-NN: Custo {vns_nn_cost:.2f}, Tempo {vns_nn_time:.4f}s, Rotas {len(vns_nn)}")

    # Clarke & Wright
    start = time.time()
    cw_solution = modified_clarke_wright_savings(customers, vehicle, depot, charging_stations)
    cw_time = time.time() - start
    cw_cost = calculate_total_cost(cw_solution)
    log.append({"method": "C&W", "cost": cw_cost, "time": cw_time, "routes": len(cw_solution)})
    print(f"Solução C&W: Custo {cw_cost:.2f}, Tempo {cw_time:.4f}s, Rotas {len(cw_solution)}")

    # VNS pós-C&W com 3 execuções (para teste rápido)
    N = 3
    vns_cw_costs = []
    vns_cw_times = []
    histories = []
    for i in range(N):
        start = time.time()
        vns_cw, history = run_vns(cw_solution, k_max=3, max_iter=50, vehicle=vehicle, stations=charging_stations)
        vns_time = time.time() - start
        vns_cw_costs.append(calculate_total_cost(vns_cw))
        vns_cw_times.append(vns_time)
        histories.append(history)
    vns_cw_mean_cost = statistics.mean(vns_cw_costs)
    vns_cw_std_cost = statistics.stdev(vns_cw_costs)
    vns_cw_mean_time = statistics.mean(vns_cw_times)
    log.append({"method": "VNS pos-C&W", "cost_mean": vns_cw_mean_cost, "cost_std": vns_cw_std_cost, "time_mean": vns_cw_mean_time, "routes": len(vns_cw)})

    print("VNS pós-C&W (5 execuções):")
    print(f"Custo Médio: {vns_cw_mean_cost:.2f} ± {vns_cw_std_cost:.2f}, Tempo Médio: {vns_cw_mean_time:.4f}s")

    # Tabela de Comparação
    print("\n--- Tabela de Comparação ---")
    print(f"{'Método':<15} {'Custo':<10}")
    print("-" * 25)
    print(f"{'NN':<15} {nn_cost:<10.2f}")
    print(f"{'C&W':<15} {cw_cost:<10.2f}")
    print(f"{'VNS pos-NN':<15} {vns_nn_cost:<10.2f}")
    print(f"{'VNS pos-C&W':<15} {vns_cw_mean_cost:<10.2f}")
    print(f"Melhoria NN->VNS: {((nn_cost - vns_nn_cost) / nn_cost * 100):.2f}%")
    print(f"Melhoria C&W->VNS: {((cw_cost - vns_cw_mean_cost) / cw_cost * 100):.2f}%")

    # Gráfico de Benchmark
    methods = ['NN', 'C&W', 'VNS pos-NN', 'VNS pos-C&W']
    costs = [nn_cost, cw_cost, vns_nn_cost, vns_cw_mean_cost]
    plt.bar(methods, costs, color=['red', 'blue', 'green', 'purple'])
    plt.title('Comparação de Custos')
    plt.ylabel('Custo Total')
    plt.savefig('benchmark_comparison.png')
    print("Gráfico salvo em benchmark_comparison.png")

    # Gráfico de Convergência
    plot_convergence(histories)

    # Salvar log
    with open('performance_log.json', 'w') as f:
        json.dump(log, f, indent=2)
    print("Log salvo em performance_log.json")