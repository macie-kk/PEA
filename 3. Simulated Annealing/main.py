from src.utils import read_matrix, load_config, str_to_tuple, round_seconds
from src.solver import solve_tsp
from src.logger import Logger
from src.constants import INPUT_DIR, OUTPUT_DIR

import sys


def main():
    cfg = load_config()   
    output = run_solve(cfg)
    # save_to_file(cfg, output)


def run_solve(cfg: dict):
    print('[OK] Rozwiazywanie\n')

    repeats = cfg['Repeats']
    matrix = read_matrix(f'{INPUT_DIR}/{cfg["Input_File"]}')

    # zapisywanie wszystkich znalezionych rozwiazan
    outputs = []
    for i in range(repeats):
        if i > 1: print(f'[{i+1}/{repeats}]      ', end='\r')
        outputs.append(solve_tsp(matrix, cfg))
        
    # szkielet obiektu wyjsciowego
    final_output = {
        'input_file': cfg['Input_File'],
        'repeats': repeats,
        'times': [],
        'solution': float('inf'),
        'path': (),
    }

    # znajdowanie najlepszego rozwiazania i sciezki sposrod wszystkich powtorzen
    for output in outputs:
        working_time = round_seconds(output['time'], cfg['Precision'])
        final_output['times'].append(working_time)

        # wybor najlepszego znalezionego rozwiazania
        solution = output['solution']
        if solution < final_output['solution']:
            final_output['solution'] = solution
            final_output['path'] = output['path']


    # dopisanie danych do zapisu
    final_output['input_file'] = cfg['Input_File']
    final_output['repeats'] = repeats

    print('Rozwiazanie: ', final_output['solution'])
    print('Sciezka: ', final_output['path'])
    print(f'\n--> Dokladnosc: {round(cfg["Solution"]/final_output["solution"] * 100)}%')
    print(f'--> Czas: {round(sum(final_output["times"]), 2)}s')

    return output


def save_to_file(cfg: dict, output: dict):
    logger = Logger(OUTPUT_DIR, cfg['Output_File'])
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
