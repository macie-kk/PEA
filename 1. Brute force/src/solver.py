import itertools
import math
import time


def solve_tsp(stop_1m: bool, matrix: list[list]):
    paths = itertools.permutations(range(len(matrix[0])))  # [(0, 1, 2), (0, 2, 1), ...]

    shortest = {
        'path': (),
        'solution': float('inf')
    }

    total_paths = math.factorial(len(matrix[0]))

    start_time = time.time()
    saved_start_time = time.time_ns()
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
            eta = int((total_paths - path_i) / its_per_second)
            total = int(time.time() - start_time)

            if stop_1m and total >= 60:
                shortest['time'] = eta + total
                shortest['path'] = 'NULL'
                shortest['solution'] = 'NULL'
                return shortest

            print(f'Checking [{path_i + 1}/{total_paths}] :: {its_per_second}[it]/s :: ETA: {eta}s :: Total: {total}s      ', end='\r')

        path_value = 0
        path_len = len(path)
        for i in range(path_len-1):
            # (0, 1, 2, 3, 4, 5)
            current_point = path[i]
            next_point = path[i + 1]
            path_value += matrix[current_point][next_point]

            if path_value >= shortest['solution']:
                break

        path_value += matrix[path[path_len-1]][path[0]]

        if path_value < shortest['solution']:
            shortest['solution'] = path_value
            shortest['path'] = path + (path[0],)

    shortest['time'] = round((time.time_ns() - saved_start_time) * 10**(-9), 7)
    return shortest
