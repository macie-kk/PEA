from fileinput import filename
import os


class Logger:
    def __init__(self, file_name):
        self.output_dir = './output'
        self.output_path = f'{self.output_dir}/{file_name}'

    def log(self, output):
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        if not os.path.exists(self.output_path):
            with open(self.output_path, 'w') as f:
                f.write('instancja\tliczba_wykonan\trozwiazanie\tsciezka\tczasy[s]\n')

        with open(self.output_path, 'a+') as f:
            f.write(f'{output["test_file"]}\t{output["repeats"]}\t{output["solution"]}\t{output["path"]}\t{";".join(output["times"])}\n')
