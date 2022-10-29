import os


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
        config[key_value_split[0]] = comment_split[0].strip()

    return config


# parsowanie stringa ze sciezka "(1, 2, 3, 4)" na obiekt tuple
def parse_string_path(string):
    tuple_ex = Exception(f'Podana wartosc "{string}" nie jest poprawnym tuplem')
    try:
        s = eval(string)
        if type(s) == tuple:
            return s
        raise tuple_ex
    except:
        raise tuple_ex 


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
            print(val, end=' ')
        print()


# zwracanie tablicy z liniami danego pliku
def get_file_lines(filepath: str):
    if not os.path.exists(filepath):
        raise Exception(f"File doesn't exist: '{filepath}'")

    with open(filepath, 'r') as f:
        return f.read().splitlines()
