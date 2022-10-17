def load_config():
    config = {}
    lines = get_file_lines('config.ini')
    for line in lines:
        split = line.split('=')
        config[split[0]] = split[1]
    return config


def read_matrix(filepath: str):
    lines = get_file_lines(filepath)
    matrix = [[] for _ in range(len(lines))]

    for i, line in enumerate(lines):
        values = " ".join(line.split()).split(' ')  # remove multiple spaces from line & split by columns

        if len(values) == 1:
            continue

        for v in values:
            matrix[i].append(v)

    return matrix


def print_matrix(matrix: list[list]):
    for row in matrix:
        for val in row:
            print(val + ' ', end='')
        print()


def get_file_lines(filepath: str):
    with open(filepath, 'r') as f:
        return f.read().splitlines()
