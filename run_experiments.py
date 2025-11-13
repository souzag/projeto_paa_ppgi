import subprocess
import json
import os

# Experimentos: diferentes tamanhos e seeds (teste com 2)
experiments = [
    (50, 5, 42),
    (70, 7, 44)
]

all_logs = []

for num_customers, num_stations, seed in experiments:
    print(f"Executando experimento: {num_customers} clientes, {num_stations} estações, seed {seed}")
    # Chamar main.py com argumentos
    result = subprocess.run(['python', 'main.py', str(num_customers), str(num_stations), str(seed)],
                            capture_output=True, text=True, cwd=os.getcwd())
    if result.returncode == 0:
        print("Sucesso")
        # Carregar log gerado
        log_file = 'performance_log.json'
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                log = json.load(f)
            log.append({"experiment": f"{num_customers}_{num_stations}_{seed}"})
            all_logs.extend(log)
    else:
        print(f"Erro: {result.stderr}")

# Salvar logs cumulativos
with open('cumulative_performance_log.json', 'w') as f:
    json.dump(all_logs, f, indent=2)

print("Logs cumulativos salvos em cumulative_performance_log.json")