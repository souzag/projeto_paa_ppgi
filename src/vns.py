import random
import copy
from .utils import calculate_total_cost
from .neighborhoods import apply_relocate, apply_swap, apply_2_opt, apply_relocate_station, apply_swap_station

def shake(solution, k, vehicle, stations):
    current = copy.deepcopy(solution)
    operators = [apply_relocate, apply_swap, apply_2_opt, apply_relocate_station, apply_swap_station]
    for _ in range(k):
        op = random.choice(operators)
        if 'station' in op.__name__:
            current = op(current, vehicle, stations)
        else:
            current = op(current, vehicle)
    return current

def local_search(solution, vehicle, stations):
    current = copy.deepcopy(solution)
    improved = True
    operators = [apply_relocate, apply_swap, apply_2_opt, apply_relocate_station, apply_swap_station]
    while improved:
        improved = False
        for op in operators:
            if 'station' in op.__name__:
                new_sol = op(current, vehicle, stations)
            else:
                new_sol = op(current, vehicle)
            if calculate_total_cost(new_sol) < calculate_total_cost(current):
                current = new_sol
                improved = True
                break  # First improvement
    return current

def run_vns(initial_solution, k_max, max_iter, vehicle, stations=None):
    if stations is None:
        stations = []
    current = copy.deepcopy(initial_solution)
    history = [calculate_total_cost(current)]
    k = 1
    for _ in range(max_iter):
        shaken = shake(current, k, vehicle, stations)
        local = local_search(shaken, vehicle, stations)
        if calculate_total_cost(local) < calculate_total_cost(current):
            current = local
            k = 1
        else:
            k += 1
            if k > k_max:
                k = 1
        history.append(calculate_total_cost(current))
    return current, history