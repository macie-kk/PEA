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
    # for ns in ['Swap', 'Closest']         # neighbor search

    for sp in ['Greedy', 'Natural', 'Random']:
        for file in inputs:
            config = {
                'Start_Path': sp,
                'Output_File': f'tsp_results_start-path-{sp}.tsv',
                'Input_File': file['file'],
                'Solution': file['solution']
            }
            main(config)


# burma14.tsp:3323, gr17.tsp:2085, gr21.tsp:2707, gr24.tsp:1272, bays29.tsp:2020, ftv33.atsp:1286, ftv44.atsp:1613, ft53.atsp:6905, ftv70.atsp:1950, ch150.tsp:6528, ftv170.atsp:2755, gr202.tsp:40160, rbg323.atsp:1326, pcb442.tsp:50778, rbg443.atsp:2720, gr666.tsp: 294538, pr1002.tsp:259045, pr2392.tsp:378032
def get_inputs():
    return [
        {
            'file': 'burma14.tsp',
            'solution': 3323,
        },
        {
            'file': 'gr17.tsp',
            'solution': 2085,
        },
        {
            'file': 'gr21.tsp',
            'solution': 2707,
        },
        {
            'file': 'gr24.tsp',
            'solution': 1272,
        },
        {
            'file': 'bays29.tsp',
            'solution': 2020,
        },
        {
            'file': 'ftv33.atsp',
            'solution': 1286,
        },
        {
            'file': 'ftv44.atsp',
            'solution': 1613,
        },
        {
            'file': 'ft53.atsp',
            'solution': 6905,
        },
        {
            'file': 'ftv70.atsp',
            'solution': 1950,
        },
        {
            'file': 'ch150.tsp',
            'solution': 6528,
        },
        {
            'file': 'ftv170.atsp',
            'solution': 2755,
        },
        {
            'file': 'gr202.tsp',
            'solution': 40160,
        },
        {
            'file': 'rbg323.atsp',
            'solution': 1326,
        },
        {
            'file': 'pcb442.tsp',
            'solution': 50778,
        },
        {
            'file': 'rbg443.atsp',
            'solution': 2720,
        },
        {
            'file': 'gr666.tsp',
            'solution': 294538,
        },
        {
            'file': 'pr1002.tsp',
            'solution': 259045,
        },
        {
            'file': 'pr2392.tsp',
            'solution': 378032,
        },
    ]


if __name__ == '__main__':
    run_test()
