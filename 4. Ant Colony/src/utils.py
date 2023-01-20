import os
import tsplib95

# ladowanie konfiguracji
# format: Klucz=Wartosc # komentarz
def load_config():
    config = {}
    lines = get_file_lines('config.ini')
    for line in lines:
        if line.startswith('#') or len(line.strip()) == 0: # pomijanie pustych linii i komentarzy
            continue

        key_value_split = line.split('=')               # rozdzielenie klucza i wartosci
        comment_split = key_value_split[1].split('#')   # rozdzielenie wartosci i komentarza
        config[key_value_split[0]] = parse(comment_split[0].strip())

    return config


def round_seconds(time_ns: int, precision: int):
    return round(time_ns * 10**(-9), precision)


# parsowanie stringa to odpowiedniego typu danych [bool, int, float, str]
def parse(value):
    if value in ['True', 'False']:
        return value == 'True'

    try:
        num = int(value)
        return num
    except: pass

    try:
        num = float(value)
        return num
    except: pass

    if value == '':
        return None

    return value


# parsowanie stringa na obiekt tuple
def str_to_tuple(string: str):
    string = string.replace('(', '').replace(')', '')
    string = string.split(',')
    
    values = []
    for val in string:
        values.append(parse(val.strip()))

    return tuple(values) 


# wczytywanie macierzy
def read_matrix(filepath: str):
    if filepath.split('.')[-1] == 'txt':
        lines = get_file_lines(filepath)
        lines = [line for line in lines if len(line.strip().split(' ')) > 1]  # usuwanie pustych linii

        matrix = [[] for _ in range(len(lines))]  # inicjalizacja macierzy 2D

        for i, line in enumerate(lines):
            values = " ".join(line.split()).split(' ')  # usuwanie zbednych spacji i rozdzial wartosci

            if len(values) == 1 or len(values) == 0:
                continue

            # wpisywanie do macierzy
            for v in values:
                matrix[i].append(int(v))

        return matrix
    
    ############## TSPLIB FORMAT ##############
    
    problem = tsplib95.load(filepath)
    size_range = range(len(list(problem.get_nodes())))

    matrix = [[] for _ in size_range]  # inicjalizacja macierzy 2D

    for i in size_range:
        for j in size_range:
            matrix[i].append(problem.get_weight(i, j))

    return matrix


# wypisywanie macierzy
def print_matrix(matrix: list):
    for row in matrix:
        for val in row:
            print(val, end=' ')
        print()


# zwracanie tablicy z liniami danego pliku
def get_file_lines(filepath: str):
    if not os.path.exists(filepath):
        raise Exception(f"File doesn't exist: '{filepath}'")

    with open(filepath, 'r') as f:
        return f.read().splitlines()
