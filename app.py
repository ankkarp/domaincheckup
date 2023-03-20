import argparse

from adapter import CheckupAdapter
from checkup import DomainCheckup


parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', help='Путь к входному файлу')
args = parser.parse_args()


class App:
    def __init__(self):
        pinger = DomainCheckup()
        self.adapter = CheckupAdapter(pinger)

    def checkfile(self, input_path):
        self.adapter.checkup(input_path)


if __name__ == "__main__":
    app = App()
    app.checkfile(input_path=args.file)
