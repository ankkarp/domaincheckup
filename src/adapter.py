class CheckupAdapter:
    def __init__(self, checkup):
        self.checkup = checkup

    def __call__(self):
        self.checkup()
