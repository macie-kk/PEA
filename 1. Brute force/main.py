from src.utils import read_matrix, load_config
from src.solver import solve_tsp
from src.logger import Logger
from src.constants import INPUT_DIR, OUTPUT_DIR


def main():
    # ladowanie configu
    config = load_config()
    repeats = int(config['Repeats'])
    stop_1m = bool(config['Stop_After_1m'])
    input_file = config['Input_File']

    # wczytywanie macierzy i inicjalizacja loggera wynikow
    matrix = read_matrix(f'{INPUT_DIR}/{input_file}')
    logger = Logger(OUTPUT_DIR, config['Output_File'])

    # rozwiazywanie problemu n razy
    output = {}
    times = []
    for _ in range(repeats):
        output = solve_tsp(stop_1m, matrix)
        times.append(str(output['time']).replace('.', ','))

    # dopisanie danych do zapisu
    output['test_file'] = input_file
    output['repeats'] = repeats
    output['times'] = times

    print('\nWartosc optymalna: ', output['solution'])
    print('Sciezka optymalna: ', output['path'])
    print('Czasy: ', output['times'])

    # zapisywanie wynikow
    logger.log(output)
    print('\n[OK] Done')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        input('\n[!] Error:', e, end='\n\n')
