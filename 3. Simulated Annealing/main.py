from src.utils import read_matrix, load_config, round_seconds
from src.solver import solve_tsp
from src.logger import Logger
from src.constants import INPUT_DIR, OUTPUT_DIR
import sys


def main(cfg: dict = None):
    if cfg is None:
        cfg = load_config()

    output = run_solve(cfg)
    save_to_file(cfg, output)


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
    final_output = get_output_struct(cfg)

    # znajdowanie najlepszego rozwiazania i sciezki sposrod wszystkich powtorzen
    for output in outputs:
        final_output['time'] += output['time']

        # wybor najlepszego znalezionego rozwiazania
        solution = output['solution']
        if solution < final_output['solution']:
            final_output['solution'] = solution
            final_output['path'] = output['path']

    # dokladnosc znalezionego rozwiazania na podstawie optymalnego + zaokraglony czas pracy
    final_output['accuracy']  = round(cfg["Solution"]/final_output["solution"] * 100)    
    final_output['time'] = str(round_seconds(final_output['time'], cfg['Precision'])).replace('.', ',')

    print_results(final_output, cfg)
    return final_output


def get_output_struct(cfg):
    return {
        'input_file': cfg['Input_File'],
        'repeats': cfg['Repeats'],
        'solution': float('inf'),
        'accuracy': 0,
        'path': (),
        'temp': cfg['Temperature'],
        'cooling_rate': cfg['Cooling_Rate'],
        'cooling_type': cfg['Cooling_Type'],
        'epochs': cfg['Epochs'],
        'time': 0,
    }


def print_results(final_output: dict, cfg: dict):
    print('Rozwiazanie: ', final_output['solution'])
    print('Sciezka: ', final_output['path'])

    if cfg['Solution'] is not None:
        print(f'\n--> Dokladnosc: {final_output["accuracy"]}%')
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
