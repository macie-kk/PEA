from fileinput import filename
import os


class Logger:
    def __init__(self, out_dir, file_name):
        self.output_dir = out_dir
        self.output_path = f'{out_dir}/{file_name}'

    def get_fields(self, output: dict):
        return {
            'instancja': output['input_file'],
            'l_wykonan': output["repeats"],
            'naj_rozw.': output["solution"],
            'dokladnosc [%]': output["accuracy"],
            'sredni_blad [%]': output["avg_error"],
            'czas [s]': output["time"],
            'ants': output['ants'],
            'iteracje': output['iterations'],
            'alpha': output['alpha'],
            'beta': output['beta'],
            'rho': output['rho'],
            'tau': output['tau'],
            'Q': output['Q'],
            'algorytm': output['Algorithm'],
            'naj_sciezka': output["path"],
        }

    def get_header(self, fields: dict) -> str:
        header = ''
        for field in fields:
            header += f'{field}\t'
        header += '\n'

        return header

    # tworzenie pliku wyjsciowego i wiersza naglowkowego

    def write_header(self, header: str):
        with open(self.output_path, 'w') as f:
            f.write(header)

    # zapisywanie danych do pliku rozdzielonych tabulatorem -- czasy rozdzielone srednikiem

    def write_fields(self, fields):
        fields_line = ''
        for field in fields:
            fields_line += f'{fields[field]}\t'
        fields_line += '\n'

        with open(self.output_path, 'a') as f:
            f.write(fields_line)

    def log(self, output: dict):
        # tworzenie folderu wyjsciowego
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        fields = self.get_fields(output)
        header = self.get_header(fields)

        if not os.path.exists(self.output_path):
            self.write_header(header)

        self.write_fields(fields)
