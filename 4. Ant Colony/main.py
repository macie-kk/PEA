import sys

from src.constants import INPUT_DIR, OUTPUT_DIR
from src.logger import Logger
from src.solver import solve_tsp
from src.utils import load_config, read_matrix, round_seconds, str_to_tuple


def main(override_cfg: dict = None):
    cfg = load_config()

    # nadpisz wybrane klucze configu
    if override_cfg is not None:
        for key in override_cfg:
            cfg[key] = override_cfg[key]

    inputs = str_to_tuple(cfg['Input_Files'])
    for input_f in inputs:
        col_split = input_f.split(':')

        solution = None
        filename = col_split[0].strip()
        try:
            solution = int(col_split[1].strip())
        except:
            pass

        output = run_solve(cfg, filename, solution)
        save_to_file(cfg, output)


def run_solve(cfg: dict, cfg_input: str, cfg_solution: int):
    print(f'\n[OK] Rozwiazywanie: {cfg_input}\n')

    repeats = cfg['Repeats']
    matrix = read_matrix(f'{INPUT_DIR}/{cfg_input}')

    # zapisywanie wszystkich znalezionych rozwiazan
    outputs = []
    for i in range(repeats):
        if repeats > 1:
            print(f'[{i+1}/{repeats}]      ', end='\r')
        outputs.append(solve_tsp(matrix, cfg))

    # szkielet obiektu wyjsciowego
    final_output = get_output_struct(cfg)
    final_output['input_file'] = cfg_input

    errors = []
    # znajdowanie najlepszego rozwiazania i sciezki sposrod wszystkich powtorzen
    for output in outputs:
        final_output['time'] += output['time']

        # wybor najlepszego znalezionego rozwiazania
        solution = output['solution']
        errors.append(round((1 - cfg_solution/solution) * 100) if cfg_solution is not None else '---')
        if solution < final_output['solution']:
            final_output['solution'] = solution
            final_output['path'] = output['path']

    # dokladnosc znalezionego rozwiazania na podstawie optymalnego + zaokraglony czas pracy
    final_output['accuracy'] = round(cfg_solution/final_output["solution"] * 100) if cfg_solution is not None else '---'
    final_output['time'] = round_seconds(final_output['time'], cfg['Precision'])
    final_output['avg_error'] = sum(errors)/len(errors) if cfg_solution is not None else '---'

    print_results(final_output, cfg_solution)
    return final_output


def get_output_struct(cfg):
    return {
        'repeats': cfg['Repeats'],
        'solution': float('inf'),
        'accuracy': 0,
        'avg_error': 0,
        'path': (),
        'time': 0,
        'ants': cfg['Ants'],
        'iterations': cfg['Iterations'],
        'alpha': cfg['Alpha'],
        'beta': cfg['Beta'],
        'rho': cfg['Rho'],
        'tau': cfg['Tau'],
        'Q': cfg['Q'],
        'Algorithm': cfg['Algorithm'],
    }


def print_results(final_output: dict, cfg_solution: int):
    print('Rozwiazanie: ', final_output['solution'])
    print('Sciezka: ', final_output['path'])

    if cfg_solution is not None:
        print(f'\n--> Dokladnosc: {final_output["accuracy"]}%')
        print(f'--> Sredni blad: {final_output["avg_error"]}%')
    print(f'--> Czas: {final_output["time"]}s')


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
