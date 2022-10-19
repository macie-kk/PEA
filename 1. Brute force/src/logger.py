from fileinput import filename
import os


class Logger:
    def __init__(self, out_dir, file_name):
        self.output_dir = out_dir
        self.output_path = f'{out_dir}/{file_name}'

    def log(self, output):
        # tworzenie folderu wyjsciowego
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        # tworzenie pliku wyjsciowego i wiersza naglowkowego
        if not os.path.exists(self.output_path):
            with open(self.output_path, 'w') as f:
                f.write('instancja\tliczba_wykonan\trozwiazanie\tsciezka\tczasy[s]\n')

        # zapisywanie danych do pliku rozdzielonych tabulatorem -- czasy rozdzielone srednikiem
        with open(self.output_path, 'a+') as f:
            f.write(f'{output["test_file"]}\t{output["repeats"]}\t{output["solution"]}\t{output["path"]}\t{";".join(output["times"])}\n')
