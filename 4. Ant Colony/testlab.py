from main import main

'''
    Plik do testowania zaleznosci roznych parametrow
    i zapisywaniu w dedykowanym pliku
'''


def run_test():
    inputs = get_inputs()

    # for a in [0.1, 1, 5]:

    for b in [0.1, 1, 5]:
        for file in inputs:
            ants = file.get('Ants', 0)
            iter = file.get('Iterations', 30)
            repeats = file.get('repeats', 1)

            config = {
                'Beta': b,
                'Output_File': f'tsp_results_beta-{b}.tsv',
                'Input_Files': f'({file["file"]}:{file["solution"]})',
                'Ants': ants,
                'Iterations': iter,
                'Repeats': repeats,
            }
            main(config)

    for r in [0.1, 0.5, 0.9]:
        for file in inputs:
            ants = file.get('Ants', 0)
            iter = file.get('Iterations', 30)
            repeats = file.get('repeats', 1)

            config = {
                'Rho': r,
                'Output_File': f'tsp_results_rho-{r}.tsv',
                'Input_Files': f'({file["file"]}:{file["solution"]})',
                'Ants': ants,
                'Iterations': iter,
                'Repeats': repeats,
            }
            main(config)

    for ph in ['QAS', 'DAS', 'CAS']:
        for file in inputs:
            ants = file.get('Ants', 0)
            iter = file.get('Iterations', 30)
            repeats = file.get('repeats', 1)

            config = {
                'Ph_Decay': ph,
                'Output_File': f'tsp_results_ph-decay-{ph}.tsv',
                'Input_Files': f'({file["file"]}:{file["solution"]})',
                'Ants': ants,
                'Iterations': iter,
                'Repeats': repeats,
            }
            main(config)

# burma14.tsp:3323, gr24.tsp:1272, ftv44.atsp:1613, ftv70.atsp:1950, ch150.tsp:6528, gr202.tsp:40160, rbg323.atsp:1326, pcb442.tsp:50778, gr666.tsp: 294538, pr1002.tsp:259045, pr2392.tsp:378032


def get_inputs():
    return [
        {
            'file': 'burma14.tsp',
            'solution': 3323,
            'repeats': 5,
        },
        {
            'file': 'gr24.tsp',
            'solution': 1272,
            'repeats': 5,
        },
        {
            'file': 'ftv44.atsp',
            'solution': 1613,
            'repeats': 5,
        },
        {
            'file': 'ftv70.atsp',
            'solution': 1950,
            'repeats': 5,
        },
        {
            'file': 'ch150.tsp',
            'solution': 6528,
            'Ants': 50,
            'repeats': 1,
        },
        {
            'file': 'gr202.tsp',
            'solution': 40160,
            'Ants': 20,
            'Iterations': 5,
        },
        {
            'file': 'rbg323.atsp',
            'solution': 1326,
            'Ants': 20,
            'Iterations': 5,
        },
        {
            'file': 'pcb442.tsp',
            'solution': 50778,
            'Ants': 10,
            'Iterations': 5,
        },
        {
            'file': 'gr666.tsp',
            'solution': 294538,
            'Ants': 5,
            'Iterations': 5,
        },
        {
            'file': 'pr1002.tsp',
            'solution': 259045,
            'Ants': 3,
            'Iterations': 3,
        },
        {
            'file': 'pr2392.tsp',
            'solution': 378032,
            'Ants': 2,
            'Iterations': 2,
        },
    ]


if __name__ == '__main__':
    run_test()
