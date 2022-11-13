import itertools


def solve_tsp(matrix: list):
    cost = {}
    S = list(range(1, len(matrix)))
    P = {}

    for k in S:
        cost[(k, (k,))] = matrix[0][k]

    for k in range(2, len(S) + 1):
        subsets = itertools.combinations(S, k)

        for set in subsets:
            for xi in set:
                new_set = tuple(x for x in set if x != xi)

                costs = []
                min_cost = float('inf')
                min_pre_v = None    # wierzcholek poprzedzajacy minimalny koszt
                min_pre_s = None    # sciezka poprzedzajaca minimalny koszt

                for xj in new_set:
                    costs.append(cost[(xj, new_set)] + matrix[xj][xi])
                    if costs[-1] < min_cost:
                        min_cost = costs[-1]
                        min_pre_v = xj
                        min_pre_s = (xj, new_set)
                        
                
                # print(f'cost({xi}, {set}) = min({costs}) = {min_cost} [{min_pre}]')
                cost[(xi, set)] = min_cost
                P[(xi, set)] = {'v': min_pre_v, 's': min_pre_s} # zapisanie informacji o poprzedzajacym wierzcholku i sciezce

    for c in cost:
        if len(c[1]) == len(S):
            cost[c] += matrix[c[0]][0]
        # print(c, ':', cost[c], '::', P.get(c))

    solution, path = backtracking(cost, P, S)

    # print('----------------')
    # print('Wynik:', solution)
    # print('Sciezka:', path)

    return {
        'time': None,
        'solution': solution,
        'path': tuple(path)
    }

def backtracking(cost: dict, P: dict, S: list):
    cost_keys = list(cost)              # lista kluczy kosztow -- (xi, S)
    max_len_sets = cost_keys[-len(S):]  # lista najdluzszych zestawow

    solution = float('inf')
    last_pre_v = None       # ostatni wierzcholek poprzedzajacy
    last_pre_s = None       # ostatnia sciezka poprzedzajaca

    # znalezienie rozwiazania z najwiekszych zbiorow oraz poprzedzajacego je wierzcholka i sciezki
    for key in max_len_sets:
        if cost[key] < solution:
            solution = cost[key]
            last_pre_v = key[0]
            last_pre_s = key

    path = [0, last_pre_v]

    # backtracking po zapisanych poprzedzajacych wierzcholkach i sciezkach
    cost_keys.reverse()
    current_set = last_pre_s
    while True:
        if len(current_set[1]) == 1:
            break
        path.append(P[current_set]['v'])
        current_set = P[current_set]['s']
    path.append(0)

    return solution, path