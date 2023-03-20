import pandas as pd
import json
from datetime import datetime

from datetime import datetime


class Writer:
    def __init__(self, filename='res.json'):
        self.filename = filename

    def __call__(self, data):
        with open(self.filename, 'w+') as outfile:
            json.dump(data, outfile)
