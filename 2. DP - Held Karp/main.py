from src.utils import read_matrix, load_config, str_to_tuple
from src.solver import solve_tsp
from src.logger import Logger
from src.constants import INPUT_DIR, OUTPUT_DIR

import sys


def main():
    # ladowanie configu
    config = load_config()
    testing = config['Test'] == 'True'

    if testing:
        run_test(config)
        return
    
    output = run_solve(config)
    save_to_file(config, output)


def run_test(config: dict):
    print('[OK] Testowanie\n')

    file = config['Test_File']
    solution = int(config['Test_Solution'])
    path = str_to_tuple(config['Test_Path'])

    matrix = read_matrix(f'{INPUT_DIR}/{file}')
    result = solve_tsp(matrix)

    solution_match = solution == result['solution']
    path_match = path == result['path'] or path == tuple(reversed(result['path']))

    print('[✓]' if solution_match else '[✗]', end=' ')
    print(f'Wynik: {result["solution"]}', end='\n' if solution_match else f' -- Poprawne: {solution}\n')
    
    print('[✓]' if path_match else '[✗]', end=' ')
    print(f'Sciezka: {result["path"]}', end='\n' if path_match else f' -- Poprawne: {path}\n')
    
    print(f'--> Czas: {result["time"]} [s]')


def run_solve(config: dict):
    print('[OK] Rozwiazywanie\n')

    repeats = int(config['Repeats'])
    input_file = config['Input_File']

    matrix = read_matrix(f'{INPUT_DIR}/{config["Input_File"]}')

    output = {}
    times = []
    for i in range(repeats):
        print(f'[{i+1}/{repeats}]      ', end='\r')
        output = solve_tsp(matrix)
        times.append(str(output['time']).replace('.', ','))

    # dopisanie danych do zapisu
    output['input_file'] = input_file
    output['repeats'] = repeats
    output['times'] = times

    print('Wartosc optymalna: ', output['solution'])
    print('Sciezka optymalna: ', output['path'])
    print('Czasy: ', output['times'])

    return output


def save_to_file(config: dict, output: dict):
    logger = Logger(OUTPUT_DIR, config['Output_File'])
    logger.log(output)


if __name__ == '__main__':
    if '--debug' in sys.argv:
        main()
        sys.exit('\n[OK] Done')

    try:
        main()
        sys.exit('\n[OK] Done')
    except Exception as e:
        input(f'\n[!] Error: {e}\n')
