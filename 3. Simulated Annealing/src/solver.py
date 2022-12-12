import math
import random
import time

def solve_tsp(matrix, temperature=1, cooling_rate=0.9, max_iter = 10_000_000):
    T_MIN = 10**(-24)
    start_time = time.time_ns()

    current_path = get_random_path(matrix)
    current_cost = calc_cost(current_path, matrix)

    best_path = current_path
    best_cost = current_cost

    iter = 0
    while temperature > T_MIN:
        iter += 1
        new_path = generate_neighbor(current_path)
        new_cost = calc_cost(new_path, matrix)

        # If the new solution is better than the current solution, accept it
        if new_cost < current_cost:
            current_path = new_path
            current_cost = new_cost

            # If the new solution is also better than the best solution, update the best solution
            if new_cost < best_cost:
                best_path = new_path
                best_cost = new_cost

        # If the new solution is worse than the current solution, accept it with a probability
        # that is proportional to the difference in cost and the current temperature
        else:
            acceptance_probability = math.exp((current_cost - new_cost) / temperature)

            if random.random() < acceptance_probability:
                current_path = new_path
                current_cost = new_cost

        # Decrease the temperature according to the cooling rate
        temperature *= cooling_rate

    stop_time = time.time_ns()

    print(iter)
    return {
        'time': stop_time - start_time,
        'solution': best_cost,
        'path': (0, *best_path, 0)
    }


def calc_cost(path, matrix):
    cost = matrix[0][path[0]]
    for i in range(len(path) - 1):
        cost += matrix[path[i]][path[i + 1]]

    cost += matrix[path[-1]][0]
    return cost


def get_random_path(matrix):
    path = []
    tmp_path = [v for v in range(1, len(matrix))]
    
    for _ in range(len(tmp_path)):
        next_point = tmp_path[random.randint(0, len(tmp_path) - 1)]
        path.append(next_point)
        tmp_path.remove(next_point)

    return tuple(path)


def rand_path_v(path, _not=None):
    val = random.randint(0, len(path) - 1)
    while(val == _not):
        val = random.randint(0, len(path) - 1)

    return val

def generate_neighbor(path):
    path = list(path)
    index_1 = rand_path_v(path)
    index_2 = rand_path_v(path, _not=index_1)

    path[index_1], path[index_2] = path[index_2], path[index_1]

    return tuple(path)
