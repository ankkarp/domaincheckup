class CheckupAdapter:
    def __init__(self, checkup, reader, writer):
        self.checkup = checkup
        self.reader = reader
        self.writer = writer

    def check_file(self, filepath):
        data = self.reader.load_file(filepath)
        responses = self.checkup(data)
        return self.writer(responses)
