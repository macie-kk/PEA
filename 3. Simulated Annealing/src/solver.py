import math
import random
import time

def solve_tsp(matrix, config):
    temperature, cooling_rate, max_epochs = config['Temperature'], config['Cooling_Rate'], config['Epochs']
    T_MIN = 0.0001
    
    start_time = time.time_ns()

    current_path = get_random_path(matrix)
    current_cost = calc_cost(current_path, matrix)

    best_path = current_path
    best_cost = current_cost

    epoch = 0
    while temperature > T_MIN and epoch < max_epochs:
        epoch += 1
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
            acceptance_probability = math.exp(-(new_cost - best_cost) / temperature)

            if random.random() < acceptance_probability:
                current_path = new_path
                current_cost = new_cost

        # Decrease the temperature according to the cooling rate
        temperature *= 1 - cooling_rate

    stop_time = time.time_ns()

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


"""
---- Metody wyboru rozwiązania w sąsiedztwie
1. Metoda losowego wyboru: losowe wybieranie jednego lub więcej rozwiązań spośród tych, które są dostępne w sąsiedztwie.
2. Metoda łańcuchowa: wybieranie jednego z dostępnych rozwiązań zgodnie z ustalonym porządkiem.
3. Metoda najbliższego sąsiada: wybieranie najlepszego rozwiązania spośród dostępnych w sąsiedztwie.
4. Metoda najlepszego sąsiada: wybieranie najlepszego rozwiązania spośród tych, które są lepsze niż obecnie posiadane.
5. Metoda wybierania względem wagi: wybieranie rozwiązania o największej wadze spośród dostępnych w sąsiedztwie.

1. Boltzmann - T(k+1) = T(k) * a gdzie a jest współczynnikiem chłodzenia
2. Cauchy - T(k+1) = T(k) / (1 + a*k) gdzie a jest współczynnikiem chłodzenia, k jest numer kroku.

"""