import os


def load_config():
    config = {}
    lines = get_file_lines('config.ini')
    for line in lines:
        split = line.split('=')
        config[split[0]] = split[1]
    return config


def read_matrix(filepath: str):
    lines = get_file_lines(filepath)

    # remove size indicator line
    if len(lines[0].split(' ')) == 1:
        lines.pop(0)

    matrix = [[] for _ in range(len(lines))]

    for i, line in enumerate(lines):
        values = " ".join(line.split()).split(' ')  # remove multiple spaces from line & split by columns

        if len(values) == 1 or len(values) == 0:
            continue

        for v in values:
            matrix[i].append(int(v))

    return matrix


def print_matrix(matrix: list[list]):
    for row in matrix:
        for val in row:
            print(val + ' ', end='')
        print()


def get_file_lines(filepath: str):
    if not os.path.exists(filepath):
        raise Exception(f"File doesn't exist: '{filepath}'")

    with open(filepath, 'r') as f:
        return f.read().splitlines()
