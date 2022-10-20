import itertools
import math
import time


def solve_tsp(stop_1m: bool, matrix: list[list]):
    # generowanie permutacji dla macierzy NxN # [(0, 1, 2), (0, 2, 1), ...]
    paths = itertools.permutations(range(len(matrix[0])))

    # obliczanie ilosci permutacji silnią
    total_paths = math.factorial(len(matrix[0]))

    start_time = time.time()            # zmienna do aktualizacji postepu i okreslania czasu dzialania
    saved_start_time = time.time_ns()   # zmienna do zapisywania ostatecznego trwania dzialania algorytmu
    timestamp = int(time.time())        # zmienna do aktualizacji postepu i okreslania czasu dzialania
    iterations = 0                      # zmienna do obliczania ilosci iteracji na sekunde
    its_per_second = 0                  # zmienna do przechowywania ilosci iteracji na sekunde
    last_30_itps = []                   # tablica do obliczania sredniej czasu z ostatnich 30 czasow iteracji na sekunde

    # obiekt z danymi wyjsciowymi
    shortest = {
        'path': (),
        'solution': float('inf')
    }

    # iteracja po wszystkich permutacjach sciezek
    for path_i, path in enumerate(paths):

        # zwiekszanie ilosci iteracji jezeli trwa ta sama sekunda
        if int(time.time()) == int(timestamp):
            iterations += 1

        # akutalizacja postepu i szacowanego czasu co sekunde
        else:
            last_30_itps.append(iterations)

            # utrzymywanie max 30 wartosci w tablicy
            if len(last_30_itps) == 60:
                last_30_itps.pop()

            its_per_second = int(sum(last_30_itps) / len(last_30_itps))
            iterations = 0                                      # resetowanie ilosci iteracji
            timestamp = time.time()                             # resetowanie timestampu
            eta = int((total_paths - path_i) / its_per_second)  # obliczanie szacowanego pozostalego czasu do zakonczenia
            total = int(time.time() - start_time)               # obliczanie czasu trwania algorytmu

            # wczesniejsze przerwanie algorytmu jezeli obecna flaga i minal czas
            if stop_1m and total >= 32:
                shortest['time'] = eta + total  # zapisanie szacowanego czasu dzialania algorytmu (pozostaly czas + czas trwania)
                shortest['path'] = 'NULL'       # nie znaleziono optymalnej sciezki
                shortest['solution'] = 'NULL'   # nie znaleziono optymalnej wagi
                return shortest

            print(f'Checking [{path_i + 1}/{total_paths}] :: {its_per_second}[it]/s :: ETA: {eta}s :: Total: {total}s      ', end='\r')

        path_value = 0
        path_len = len(path)

        # zliczanie wagi sciezki danej permutacji # (0, 1, 2), (0, 2, 1), ...
        for i in range(path_len-1):
            path_value += matrix[path[i]][path[i + 1]]

            # szybsze przerwanie jezeli przekroczylismy obecne optymalne rozwiazanie
            if path_value >= shortest['solution']:
                break

        # doliczanie wagi powrotu do punktu poczatkowego
        path_value += matrix[path[path_len-1]][path[0]]

        # jezeli znaleziono nowe optymalne rozwiazanie
        if path_value < shortest['solution']:
            shortest['solution'] = path_value
            shortest['path'] = path + (path[0],)

    # w przypadku skonczenia calego algorytmu (mniejsze macierze), zapisz czas z dokladnoscia do nanosekund
    shortest['time'] = round((time.time_ns() - saved_start_time) * 10**(-9), 7)
    return shortest
