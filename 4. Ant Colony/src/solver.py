import random
import time


def solve_tsp(matrix, config):
    # parametry
    m_size = len(matrix)                    # rozmiar macierzy
    num_ants = m_size if config['Ants'] == 0 else config['Ants']  # liczba mrówek
    num_iterations = config['Iterations']   # liczba iteracji
    alpha = config['Alpha']                 # waga feromonów
    beta = config['Beta']                   # waga odległości
    tau = config['Tau']                     # początkowa wartość feromonów

    # macierz feromonów
    pheromones = [[tau/m_size for _ in range(m_size)] for _ in range(m_size)]

    # najlepsze rozwiazanie
    best_solution = {"cities": [], "distance": float("inf")}

    start_time = time.time_ns()

    # glowna petla po iteracjach
    for _ in range(num_iterations):
        ant_solutions = []

        # petla dla kazdej mrówki
        for _ in range(num_ants):
            ant_solution = {"cities": [random.randint(0, m_size-1)], "distance": 0}

            # petla dla kazdego miasta
            while len(ant_solution["cities"]) <= m_size:
                last_city = ant_solution["cities"][-1]
                next_city = None

                # liczenie prawdopodobienstw wyboru kolejnego miasta
                probabilities = [0]*m_size
                for city in range(m_size):
                    if city not in ant_solution['cities']:
                        current_next_distance = matrix[last_city][city]
                        visibility = 1 / current_next_distance if current_next_distance != 0 else 1

                        if config['Heuristic'] == 'Home':
                            next_home_distance = matrix[city][ant_solution['cities'][0]] / (m_size - len(ant_solution['cities']))
                            visibility_sum = (current_next_distance + next_home_distance) / 2
                            visibility = 1 / visibility_sum if visibility_sum != 0 else 1

                        probabilities[city] += (pheromones[last_city][city] ** alpha) * (visibility ** beta)

                # normalizacja prawdopodobienstw
                probabilities = [x / sum(probabilities) for x in probabilities]
                r = random.random()

                # wybieranie nastepnego miasta
                for city in range(len(probabilities)):
                    if r <= probabilities[city]:
                        next_city = city
                        break
                    r -= probabilities[city]

                # dodawanie miasta i odleglosci do rozwiazania
                ant_solution["cities"].append(next_city)
                ant_solution["distance"] += matrix[last_city][next_city]

                # dodawanie odleglosci powrotu do miasta startowego
                if len(ant_solution['cities']) == m_size:
                    ant_solution["distance"] += matrix[next_city][ant_solution['cities'][0]]
                    ant_solution["cities"].append(ant_solution['cities'][0])

            # dodawanie rozwiazania do listy rozwiazan
            ant_solutions.append(ant_solution)

        # aktualizacja feromonów
        pheromones = update_pheromones(pheromones, config, matrix, ant_solutions)

        # aktualizacja najlepszego rozwiazania
        best_ant_solution = get_best_ant_solution(ant_solutions)
        if best_ant_solution['distance'] < best_solution['distance']:
            best_solution = best_ant_solution

    stop_time = time.time_ns()

    return {
        'time': stop_time - start_time,
        'solution': best_solution['distance'],
        'path': best_solution['cities']
    }


# znajlezienie najlepszego z rozwiazan mrówki
def get_best_ant_solution(ant_solutions):
    best_solution = {"cities": [], "distance": float("inf")}
    for ant_solution in ant_solutions:
        if ant_solution["distance"] < best_solution["distance"]:
            best_solution = ant_solution

    return best_solution


# aktualizacja feromonów
def update_pheromones(pheromones: list, cfg: dict, matrix: list, ant_solutions: list):
    for city_1 in range(len(pheromones)):
        for city_2 in range(len(pheromones)):
            if city_1 == city_2:
                continue

            pheromones[city_1][city_2] *= (1 - cfg['Rho'])  # zanikanie feromonów

    Q = 1
    for solution in ant_solutions:
        for i in range(len(solution['cities'])-1):
            city_1 = solution['cities'][i]
            city_2 = solution['cities'][i+1]

            if cfg['Ph_Decay'] == 'DAS':
                pheromones[city_1][city_2] += Q

            if cfg['Ph_Decay'] == 'QAS':
                pheromones[city_1][city_2] += Q/matrix[city_1][city_2] if matrix[city_1][city_2] > 0 else 1

            if cfg['Ph_Decay'] == 'CAS':
                pheromones[city_1][city_2] += Q/solution['distance']

    return pheromones
