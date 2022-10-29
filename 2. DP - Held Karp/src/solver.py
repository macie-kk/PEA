import itertools


def solve_tsp(stop_1m: bool, matrix: list):
    cost = {}
    S = list(range(1, len(matrix)))

    for k in S:
        cost[(k, (k,))] = matrix[0][k]

    for k in range(2, len(S) + 1):
        subsets = list(itertools.combinations(S, k))
        
        for set in subsets:
            for xi in set:
                newset = tuple(x for x in set if x != xi)

                costs = []
                for xj in newset:
                    costs.append(cost[(xj, newset)] + matrix[xj][xi])

                # print(f'cost({xi}, {set}) = min({costs}) = {min(costs)}')
                cost[(xi, set)] = min(costs)

    max_sets = list(cost)[-len(S):]
    solution = min([cost[c] + matrix[c[0]][0] for c in max_sets])
    print(solution)