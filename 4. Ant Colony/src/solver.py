import math
import random
import time


def solve_tsp(matrix, config):
    matrix = normalize_matrix(matrix)   # remove 0-length distances

    m_size = len(matrix)
    num_ants = config['Ants']
    num_iterations = config['Iterations']
    alpha = config['Alpha']
    beta = config['Beta']
    rho = config['Rho']

    # Initialize pheromone matrix
    pheromones = [[0.1 for _ in range(m_size)] for _ in range(m_size)]
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
                next_city_probability = 0

                for city in range(m_size):
                    if city not in ant_solution["cities"]:
                        probability = (pheromones[last_city][city] ** alpha) * ((1 / matrix[last_city][city]) ** beta)
                        if probability > next_city_probability:
                            next_city = city
                            next_city_probability = probability

                ant_solution["cities"].append(next_city)
                ant_solution["distance"] += matrix[last_city][next_city]

                if len(ant_solution['cities']) == m_size:
                    ant_solution["distance"] += matrix[next_city][ant_solution['cities'][0]]
                    ant_solution["cities"].append(ant_solution['cities'][0])

            ant_solutions.append(ant_solution)

        # Update pheromones
        for city1 in range(m_size):
            for city2 in range(m_size):
                if city1 != city2:
                    pheromones[city1][city2] *= (1 - rho)
                    for ant_solution in ant_solutions:
                        if city2 in ant_solution["cities"]:
                            pheromones[city1][city2] += (rho / ant_solution["distance"])

        # Find the best solution
        best_solution = {"cities": [], "distance": float("inf")}
        for ant_solution in ant_solutions:
            if ant_solution["distance"] < best_solution["distance"]:
                best_solution = ant_solution

    stop_time = time.time_ns()

    return {
        'time': stop_time - start_time,
        'solution': best_solution['distance'],
        'path': best_solution['cities']
    }


def normalize_matrix(matrix: list):
    ml = len(matrix)
    return [[0.00001 if matrix[i][j] <= 0 else matrix[i][j] for i in range(ml)] for j in range(ml)]
