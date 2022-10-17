import itertools
import math
import time


def solve_tsp(matrix: list[list]):
    paths = itertools.permutations(range(len(matrix[0])))  # [(0, 1, 2), (0, 2, 1), ...]

    shortest = {
        'path': (),
        'value': float('inf')
    }

    total_paths = math.factorial(len(matrix[0]))

    start_time = time.time()
    timestamp = int(time.time())
    iterations = 0
    its_per_second = 0
    last_30_itps = []

    for path_i, path in enumerate(paths):
        if int(time.time()) == int(timestamp):
            iterations += 1
        else:
            last_30_itps.append(iterations)
            if len(last_30_itps) == 30:
                last_30_itps.pop()

            its_per_second = int(sum(last_30_itps) / len(last_30_itps))
            iterations = 0
            timestamp = time.time()
            print(f'Checking [{path_i + 1}/{total_paths}] :: {its_per_second}[it]/s :: ETA: {int((total_paths - path_i) / its_per_second)}s :: Total: {int(time.time() - start_time)}s      ', end='\r')

        path_value = 0
        path_len = len(path)
        for i in range(path_len):
            # (0, 1, 2, 3, 4, 5)
            current_point = path[i]
            next_point = path[0] if i == path_len - 1 else path[i + 1]
            path_value += matrix[current_point][next_point]

            if path_value >= shortest['value']:
                break

        if path_value < shortest['value']:
            shortest['value'] = path_value
            shortest['path'] = path + (path[0],)

    print('\n\n-----------------')
    print('-- Najkrotsza sciezka:', shortest['path'])
    print('-- Odleglosc:', shortest['value'], end='\n\n')
