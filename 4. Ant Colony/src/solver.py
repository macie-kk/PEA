import random
import time


def solve_tsp(matrix, config):
    m_size = len(matrix)                    # rozmiar macierzy
    num_ants = config['Ants']               # liczba mrówek
    num_iterations = config['Iterations']   # liczba iteracji
    alpha = config['Alpha']                 # waga feromonów
    beta = config['Beta']                   # waga odległości
    rho = config['Rho']                     # współczynnik zanikania feromonów
    tau = config['Tau']                     # początkowa wartość feromonów

    # macierz feromonów
    pheromones = [[tau/m_size for _ in range(m_size)] for _ in range(m_size)]
    best_solution = {"cities": [], "distance": float("inf")}

    start_time = time.time_ns()
    for _ in range(num_iterations):
        ant_solutions = []

        # Initialize ant solutions
        for _ in range(num_ants):
            ant_solution = {"cities": [random.randint(0, m_size-1)], "distance": 0}

            while len(ant_solution["cities"]) <= m_size:
                last_city = ant_solution["cities"][-1]
                next_city = None

                probabilities = [0]*m_size
                for city in range(m_size):
                    if city not in ant_solution['cities']:
                        visibility = 1 / matrix[last_city][city] if matrix[last_city][city] != 0 else 1
                        probabilities[city] += (pheromones[last_city][city] ** alpha) * (visibility ** beta)

                probabilities = [x / sum(probabilities) for x in probabilities]
                r = random.random()

                for city in range(len(probabilities)):
                    if r <= probabilities[city]:
                        next_city = city
                        break
                    r -= probabilities[city]

                ant_solution["cities"].append(next_city)
                ant_solution["distance"] += matrix[last_city][next_city]

                if len(ant_solution['cities']) == m_size:
                    ant_solution["distance"] += matrix[next_city][ant_solution['cities'][0]]
                    ant_solution["cities"].append(ant_solution['cities'][0])

            ant_solutions.append(ant_solution)

        best_solution = get_best_solution(ant_solutions)
        pheromones = update_pheromones(pheromones, rho, ant_solutions, best_solution)

    stop_time = time.time_ns()

    return {
        'time': stop_time - start_time,
        'solution': best_solution['distance'],
        'path': best_solution['cities']
    }


def get_best_solution(ant_solutions):
    best_solution = {"cities": [], "distance": float("inf")}
    for ant_solution in ant_solutions:
        if ant_solution["distance"] < best_solution["distance"]:
            best_solution = ant_solution

    return best_solution


def update_pheromones(pheromones, rho, ant_solutions, best_solution):
    for city_1 in range(len(pheromones)):
        for city_2 in range(len(pheromones)):
            pheromones[city_1][city_2] *= (1 - rho)
            for ant_solution in ant_solutions:
                if city_1 in ant_solution['cities'] and city_2 in ant_solution['cities']:
                    pheromones[city_1][city_2] += 1/best_solution['distance']

    return pheromones
