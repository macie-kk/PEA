from main import main

'''
    Plik do testowania zaleznosci roznych parametrow
    i zapisywaniu w dedykowanym pliku
'''

def run_test():
    inputs = get_inputs()

    # for cr in [0.85, 0.9, 0.99, 0.999]    # cooling rate
    # for t in [100, 1000, 10000, 10000]    # temperature
    # for e in [1, 50, 100, 150]            # epochs
    # for cs in ['Geo', 'Lin']              # cooling schedule

    for ns in ['Swap', 'Closest']:
        for file in inputs:
            config = {
                'Neighbor_Search': ns,
                'Output_File': f'tsp_results_neighbor-search-{ns}.tsv',
                'Input_File': file['file'],
                'Solution': file['solution']
            }
            main(config)


def get_inputs():
    return [
        {
            'file': 'tsp_10.txt',
            'solution': 212
        },
        {
            'file': 'tsp_12.txt',
            'solution': 264
        },
        {
            'file': 'tsp_15.txt',
            'solution': 291
        },
        {
            'file': 'tsp_20.txt',
            'solution': 386
        },
        {
            'file': 'gr24.tsp',
            'solution': 1272
        },
        {
            'file': 'ftv35.atsp',
            'solution': 1473
        },
        {
            'file': 'ftv55.atsp',
            'solution': 1608
        },
        {
            'file': 'ftv70.atsp',
            'solution': 1950 
        },
        {
            'file': 'kro124p.atsp',
            'solution': 36230
        },
        {
            'file': 'ftv170.atsp',
            'solution': 2755
        },
        {
            'file': 'rbg323.atsp',
            'solution': 1326
        },
        {
            'file': 'rbg403.atsp',
            'solution': 2465
        }
    ]


if __name__ == '__main__':
    run_test()