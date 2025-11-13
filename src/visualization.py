import matplotlib.pyplot as plt
from .problem import Depot, ChargingStation

def plot_routes(solution, stations=None):
    colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
    plt.figure(figsize=(10, 8))
    for i, route in enumerate(solution):
        x = [n.x for n in route.nodes]
        y = [n.y for n in route.nodes]
        plt.plot(x, y, marker='o', color=colors[i % len(colors)], label=f'Rota {i+1}')
        for j, node in enumerate(route.nodes):
            if isinstance(node, Depot):
                plt.scatter(node.x, node.y, color='black', marker='s', s=100, label='Depot' if i==0 and j==0 else "")
            elif isinstance(node, ChargingStation):
                plt.scatter(node.x, node.y, color='orange', marker='^', s=100, label='Station' if i==0 and j==0 else "")
            else:
                plt.scatter(node.x, node.y, color=colors[i % len(colors)], marker='o')
    if stations:
        for s in stations:
            plt.scatter(s.x, s.y, color='orange', marker='^', s=100)
    plt.legend()
    plt.title('Rotas de Veículos')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()

def plot_convergence(histories):
    plt.figure(figsize=(10, 6))
    for i, history in enumerate(histories):
        plt.plot(history, label=f'Execução {i+1}')
    plt.title('Convergência do VNS')
    plt.xlabel('Iteração')
    plt.ylabel('Custo')
    plt.legend()
    plt.grid(True)
    plt.savefig('convergence_plot.png')
    print("Gráfico de convergência salvo em convergence_plot.png")