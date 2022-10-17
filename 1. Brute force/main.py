from src.utils import read_matrix, load_config
from src.solver import solve_tsp


def main():
    config = load_config()
    matrix = read_matrix(config['Test_File'])
    solve_tsp(matrix)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('\n[!] Error:', e, end='\n\n')
