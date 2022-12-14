from src.utils import read_matrix, load_config, round_seconds
from src.solver import solve_tsp
from src.logger import Logger
from src.constants import INPUT_DIR, OUTPUT_DIR
import sys


def main(override_cfg: dict = None):
    cfg = load_config()

    # nadpisz wybrane klucze configu
    if override_cfg is not None:
        for key in override_cfg:
            cfg[key] = override_cfg[key]
        

    output = run_solve(cfg)
    save_to_file(cfg, output)


def run_solve(cfg: dict):
    print('[OK] Rozwiazywanie\n')

    repeats = cfg['Repeats']
    matrix = read_matrix(f'{INPUT_DIR}/{cfg["Input_File"]}')

    # zapisywanie wszystkich znalezionych rozwiazan
    outputs = []
    for i in range(repeats):
        if repeats > 1: print(f'[{i+1}/{repeats}]      ', end='\r')
        outputs.append(solve_tsp(matrix, cfg))
        
    # szkielet obiektu wyjsciowego
    final_output = get_output_struct(cfg)

    errors = []
    # znajdowanie najlepszego rozwiazania i sciezki sposrod wszystkich powtorzen
    for output in outputs:
        final_output['time'] += output['time']

        # wybor najlepszego znalezionego rozwiazania
        solution = output['solution']
        errors.append(round((1 - cfg["Solution"]/solution) * 100))
        if solution < final_output['solution']:
            final_output['solution'] = solution
            final_output['path'] = output['path']

    # dokladnosc znalezionego rozwiazania na podstawie optymalnego + zaokraglony czas pracy
    final_output['accuracy'] = round(cfg["Solution"]/final_output["solution"] * 100)    
    final_output['time'] = round_seconds(final_output['time'], cfg['Precision'])
    final_output['avg_error'] = sum(errors)/len(errors)

    print_results(final_output, cfg)
    return final_output


def get_output_struct(cfg):
    return {
        'input_file': cfg['Input_File'],
        'repeats': cfg['Repeats'],
        'solution': float('inf'),
        'accuracy': 0,
        'avg_error': 0,
        'path': (),
        'time': 0,
        'temp': cfg['Temperature'],
        'cooling_rate': cfg['Cooling_Rate'],
        'cooling_schedule': cfg['Cooling_Schedule'],
        'neighbor_search': cfg['Neighbor_Search'],
        'epochs': cfg['Epochs'],
    }


def print_results(final_output: dict, cfg: dict):
    print('Rozwiazanie: ', final_output['solution'])
    print('Sciezka: ', final_output['path'])

    if cfg['Solution'] is not None:
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
