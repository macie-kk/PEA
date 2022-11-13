from src.utils import read_matrix, load_config, print_matrix, parse_string_path
from src.solver import solve_tsp
from src.logger import Logger
from src.constants import INPUT_DIR, OUTPUT_DIR


def main():
    # ladowanie configu
    config = load_config()
    testing = bool(config['Test'])

    if testing:
        run_test(config)
        return

    repeats = int(config['Repeats'])
    input_file = config['Input_File']

    # wczytywanie macierzy i inicjalizacja loggera wynikow
    matrix = read_matrix(f'{INPUT_DIR}/{input_file}')

    # rozwiazywanie problemu n razy
    output = {}
    # times = []
    for _ in range(repeats):
        output = solve_tsp(matrix)
        # times.append(str(output['time']).replace('.', ','))

    # dopisanie danych do zapisu
    # output['test_file'] = input_file
    # output['repeats'] = repeats
    # output['times'] = times

    # print('\nWartosc optymalna: ', output['solution'])
    # print('Sciezka optymalna: ', output['path'])
    # print('Czasy: ', output['times'])

    # zapisywanie wynikow
    # logger = Logger(OUTPUT_DIR, config['Output_File'])
    # logger.log(output)
    print('\n[OK] Done')

def run_test(config: dict):
    print('[OK] Testowanie\n')
    file = config['Test_File']
    solution = int(config['Test_Solution'])
    path = parse_string_path(config['Test_Path'])

    matrix = read_matrix(f'{INPUT_DIR}/{file}')
    result = solve_tsp(matrix)

    solution_match = solution == result['solution']
    path_match = path == result['path'] or path == tuple(reversed(result['path']))

    print('[✓]' if solution_match else '[✗]', end=' ')
    print(f'Wynik: {result["solution"]}', end='\n' if solution_match else f' -- Poprawne: {solution}\n')
    
    print('[✓]' if path_match else '[✗]', end=' ')
    print(f'Sciezka: {result["path"]}', end='\n' if path_match else f' -- Poprawne: {path}\n')
    pass

def run_solve():
    pass

if __name__ == '__main__':
    # try:
    main()
    # except Exception as e:
    #     input(f'\n[!] Error:{e}\n\n')
