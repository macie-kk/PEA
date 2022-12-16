from main import main

'''
    Plik do testowania zaleznosci roznych parametrow
    i zapisywaniu w dedykowanym pliku
'''

def run_test():
    settings = {
        'Temperature': (1000, 100_000, 1000),
        'Cooling_Rate': (0.9999, 0.85, -0.005),
        'Epochs': (1000, 10_000, 100),
        'Cooling_Type': ['Geo', 'Log']
    }

    default = {
        'Temperature': 10000,
        'Cooling_Rate': 0.995,
        'Epochs': float('inf'),
        'Cooling_Type': 'Geo'
    }
    

if __name__ == '__main__':
    run_test()