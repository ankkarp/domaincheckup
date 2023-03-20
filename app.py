import argparse

from src.adapter import CheckupAdapter
from src.checkup import DomainCheckup
from src.inputs import TableReader
from src.outputs import Writer


parser = argparse.ArgumentParser()
parser.add_argument('--input_file', '-i', help='Входной csv-файл', type=str)
parser.add_argument('--output_file', '-o',
                    help='Json-файл, куда нужно сохранить результаты', type=str)
parser.add_argument('--header',
                    help='Номер строки-заголовка', type=int, default=0)
args = parser.parse_args()


class App:
    def __init__(self):
        pinger = DomainCheckup()
        reader = TableReader(header_line=args.header)
        writer = Writer(args.output_file)
        self.adapter = CheckupAdapter(pinger, reader, writer)

    def checkfile(self, input_path):
        self.adapter.check_file(input_path)


if __name__ == "__main__":
    app = App()
    app.checkfile(input_path=args.input_file)
