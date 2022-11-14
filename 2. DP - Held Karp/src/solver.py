import itertools
import time
from tracemalloc import start


def solve_tsp(matrix: list):
    MATRIX_SIZE = len(matrix)
    VERTICES = list(range(1, MATRIX_SIZE))   # lista wierzcholkow z pomienieciem zerowego
    PRE = {}    # obiekt przechowujacy informacje o poprzedzajacych wierzcholkach (do odtwarzania sciezki) 
    COST = {}   # obiekt przechowujacy koszty przejscia -- { (xi, S): V } -- gdzie V to koszt przejscia z wierzcholka xi do 0-wego przechodzac przez wszystkie wierzcholki w zbiorze S dokladnie raz

    start_time = time.time_ns()

    # wczytanie pojedynczych kosztow przejscia (z kazdego wierzcholka do 0-wego)
    for k in VERTICES:
        COST[(k, (k,))] = matrix[0][k]

    # obliczenie pozostalych kosztow przejsc
    for k in range(2, MATRIX_SIZE):
        subsets = itertools.combinations(VERTICES, k)   # wszystkie kombinacje zbiorow wierzcholkow o danej dlugosci k -- [(1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4), ...]

        # dla kazdego zbioru ze zbiorow kombinacji
        for set in subsets:
            # dla kazdego wierzcholka w zbiorze
            for xi in set:
                new_set = tuple(x for x in set if x != xi)  # utworzenie nowego zbioru bez obecnie sprawdzanego wierzcholka

                min_cost = float('inf') # najmniejszy koszt przejcia
                min_pre = None          # wierzcholek i sciezka poprzedzajace najmniejszy koszt przejscia

                # dla kazdego wierzcholka w nowym zbiorze
                for xj in new_set:
                    cost = COST[(xj, new_set)] + matrix[xj][xi]  # dodanie kosztu przejscia

                    # jezeli koszt przejscia jest mniejszy niz obecnie zapisany to zapisz poprzedzajacy wierzcholek
                    if cost < min_cost:
                        min_cost = cost
                        min_pre = (xj, new_set)
                        
                COST[(xi, set)] = min_cost  # zapisanie kosztu przejscia z wierzcholka 'xi' do 0-wego przez wszystkie punktu ze zbioru 'set'
                PRE[(xi, set)] = min_pre    # zapisanie informacji o poprzedzajacym wierzcholku 'xj' i sciezce 'S\{xi}'

    solution, path = backtrack(matrix, COST, PRE, VERTICES)
    
    stop_time = time.time_ns()
    work_time = round((stop_time - start_time) * 10**(-9), 2)

    return {
        'time': work_time,
        'solution': solution,
        'path': tuple(path)
    }


def backtrack(matrix: list, COST: dict, PRE: dict, VERTICES: list):
    cost_keys = list(COST.keys())
    max_cost_keys = cost_keys[-len(VERTICES):]   # lista najdluzszych zestawow

    solution = float('inf')
    pre = None
    
    # znalezienie rozwiazania z najwiekszych zbiorow wraz z poprzedzajacym je wierzcholkiem
    for key in max_cost_keys:
        cost = COST[key] + matrix[key[0]][0]
        if cost < solution:
            solution = cost
            pre = key

    path = [0, pre[0]]

    # backtracking po zapisanych poprzedzajacych wierzcholkach
    cost_keys.reverse()
    current_set = pre
    while len(current_set[1]) != 1:
        path.append(PRE[current_set][0])
        current_set = PRE[current_set]
    path.append(0)

    return solution, path