import logging

import pandas as pd


class TableReader:
    def __init__(self, columns_sep=';', ports_sep=',', header_line=None):
        self.columns_sep = columns_sep
        self.ports_sep = ports_sep
        self.header_line = header_line
        self.domain_cleanup_regex = r"(\w+:\/\/)|(\/.+)"

    def load_file(self, filepath):
        df = pd.read_csv(filepath, sep=self.columns_sep,
                         header=self.header_line)
        n_columns = len(df.columns)
        assert n_columns == 2, f"ОШИБКА ЧТЕНИЯ ФАЙЛА! Недопустимое кол-во колонок ({n_columns} != 2)."
        domain_col = df.columns[0]
        ports_col = df.columns[1]
        df[ports_col] = df[ports_col].str.split(self.ports_sep)
        df[domain_col] = df[domain_col].str.replace(
            self.domain_cleanup_regex, '', regex=True).str.strip()
        df = df.where(pd.notnull(df), None)
        return dict(df.values)
