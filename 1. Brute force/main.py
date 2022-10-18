from src.utils import read_matrix, load_config
from src.solver import solve_tsp
from src.logger import Logger


def main():
    config = load_config()
    repeats = int(config['Repeats'])
    matrix = read_matrix(config['Test_File'])
    logger = Logger(config['Output_Name'])
    stop_1m = bool(config['Stop_After_1m'])

    output = {}

    times = []
    for _ in range(repeats):
        output = solve_tsp(stop_1m, matrix)
        times.append(str(output['time']).replace('.', ','))

    output['test_file'] = config['Test_File']
    output['repeats'] = repeats
    output['times'] = times

    logger.log(output)


if __name__ == '__main__':
    # try:
    main()
    # except Exception as e:
    #     print('\n[!] Error:', e, end='\n\n')
