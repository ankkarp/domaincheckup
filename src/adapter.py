class CheckupAdapter:
    def __init__(self, checkup, reader):
        self.checkup = checkup
        self.reader = reader

    def check_file(self, filepath):
        data = self.reader.load_file(filepath)
        self.checkup(data)
