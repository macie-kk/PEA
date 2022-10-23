import os


# ladowanie konfiguracji
def load_config():
    config = {}
    lines = get_file_lines('config.ini')
    for line in lines:
        split = line.split('=')
        config[split[0]] = split[1]

    return config


# wczytywanie macierzy
def read_matrix(filepath: str):
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


# wypisywanie macierzy
def print_matrix(matrix: list):
    for row in matrix:
        for val in row:
            print(val + ' ', end='')
        print()


# zwracanie tablicy z liniami danego pliku
def get_file_lines(filepath: str):
    if not os.path.exists(filepath):
        raise Exception(f"File doesn't exist: '{filepath}'")

    with open(filepath, 'r') as f:
        return f.read().splitlines()
