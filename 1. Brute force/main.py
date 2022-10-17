from src.utils import read_matrix, load_config


def main():
    config = load_config()
    matrix = read_matrix(config['TestFile'])

if __name__ == '__main__':
    main()
