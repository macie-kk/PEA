import math
import random
import time


def solve_tsp(matrix, config):
    # poczatkowa temperatura, schemat chlodzenia, wspolczynnik chlodzenia i ilosc epok dla kazdej iteracji
    t_init, c_schedule, c_rate, epochs = config['Temperature'], config['Cooling_Schedule'], config['Cooling_Rate'], config['Epochs']

    # bufor ostatnich wynikow i jego rozmiar
    buff = []
    max_buff_size = 1000

    # rozpoczecie pomiaru czasu
    start_time = time.time_ns()

    # wygenerowanie losowej sciezki i obliczenie jej kosztu
    current_path = get_start_path(config['Start_Path'], matrix)
    current_cost = calc_cost(current_path, matrix)

    # tymczasowe zapisanie losowej sciezki jako najlepszej
    best_path = current_path
    best_cost = calc_cost(current_path, matrix)

    # obecna i minimalna temperatura
    temperature = t_init
    t_min = 0.0001

    iteration = 0
    while temperature > t_min:
        iteration += 1

        # optymalizacja rozwiazania dla kazdej temperatury zgodnie z iloscia epok
        for _ in range(epochs):
            new_path = generate_neighbor(current_path)
            new_cost = calc_cost(new_path, matrix)

            # jezeli nowe rozwiazanie jest lepsze niz najlepsze to je zaktualizuj
            if new_cost < best_cost:
                best_cost, best_path = new_cost, new_path
                continue

            # jezeli nowe rozwiazanie jest lepsze niz lokalnie najlepsze to je zaktualizuj
            if new_cost < current_cost:
                current_cost, current_path = new_cost, new_path
                continue

            # jezeli nowe rozwiazanie jest gorsze od obecnego to zaakceptuj je z prawdopodobienstwem
            if random.random() < math.exp(-(new_cost - current_cost) / temperature):
                current_cost, current_path = new_cost, new_path

        # zmniejsz temperature zgodnie ze schematem chlodzenia
        temperature = get_new_temp(t_init, c_schedule, c_rate, iteration)

        # dodaj obecne rozwiazanie do bufora
        buff.append(best_cost)

        # jezeli przekroczyl rozmiar to usun pierwsze
        if len(buff) > max_buff_size:
            buff.pop(0)

        # jezeli wszystkie ostatnie rozwiazania sa takie same i temperatura niska przerwij dzialanie
        if sum(buff) == max_buff_size*best_cost and temperature < 1:
            break

    stop_time = time.time_ns()

    return {
        'time': stop_time - start_time,
        'solution': best_cost,
        'path': (0, *best_path, 0)
    }


def get_new_temp(t_init, schedule, rate, iteration):
    # schemat geometryczny
    if schedule == 'Geo':
        return t_init*rate**iteration

    # schemat liniowy
    if schedule == 'Lin':
        return t_init / (1 + rate * iteration)


def calc_cost(path, matrix):
    cost = matrix[0][path[0]]
    for i in range(len(path) - 1):
        cost += matrix[path[i]][path[i + 1]]

    cost += matrix[path[-1]][0]

    return cost


def get_start_path(method, matrix):
    if method == 'Natural':
        path = [v for v in range(1, len(matrix))] 
        return tuple(path)

    if method == 'Random':
        path = [v for v in range(1, len(matrix))]
        random.shuffle(path)
        return tuple(path)

    if method == 'Greedy':
        path = [random.randint(1, len(matrix) - 1)]

        for vertex in range(1, len(matrix) - 1):
            min_cost = float('inf')
            next_v = None

            for i in range(1, len(matrix)):
                if i not in path and matrix[vertex][i] < min_cost:
                    min_cost = matrix[vertex][i]
                    next_v = i
            path.append(next_v)

        return tuple(path)


def generate_neighbor(path):
    path = list(path)

    index_1, index_2 = random.sample(range(len(path)), 2)
    path[index_1], path[index_2] = path[index_2], path[index_1]

    return tuple(path)


"""
---- Metody wyboru rozwiązania w sąsiedztwie
1. Metoda losowego wyboru: losowe wybieranie jednego lub więcej rozwiązań spośród tych, które są dostępne w sąsiedztwie.
2. Metoda łańcuchowa: wybieranie jednego z dostępnych rozwiązań zgodnie z ustalonym porządkiem.
3. Metoda najbliższego sąsiada: wybieranie najlepszego rozwiązania spośród dostępnych w sąsiedztwie.
4. Metoda najlepszego sąsiada: wybieranie najlepszego rozwiązania spośród tych, które są lepsze niż obecnie posiadane.
5. Metoda wybierania względem wagi: wybieranie rozwiązania o największej wadze spośród dostępnych w sąsiedztwie.
"""
