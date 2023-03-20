import logging

import pandas as pd


class TableReader:
    def __init__(self, columns_sep=';', ports_sep=',', header_line=None):
        self.columns_sep = columns_sep
        self.ports_sep = ports_sep
        self.header_line = header_line

    # def __init__(self):
    # self.excel_regex = re.compile('.(xls[xmb]?|od[fst])$')

    # def _filter_ports(self, df):
    #     valid_ports = []
    #     for i, (host, ports) in enumerate(zip(df.values)):
    #         hostports = []
    #         for p in ports:
    #             if p.isdigit():
    #                 hostports.append(p)
    #             else:
    #                 logging.warning(
    #                     f'Введен недопустимый номер порта ({p})! Норм порта должен быть целочисленным.',
    #                     'Данный порт будет пропущен при проверке.',
    #                     f'[строка: {i}, хост: {host}]')

    #     return port.isdigit()

    def load_file(self, filepath):
        df = pd.read_csv(filepath, sep=self.columns_sep,
                         header=self.header_line)
        n_columns = len(df.columns)
        assert n_columns == 2, f"ОШИБКА ЧТЕНИЯ ФАЙЛА! Недопустимое кол-во колонок ({n_columns} != 2)."
        ports_col = df.columns[1]
        # split ports into list
        df[ports_col] = df[ports_col].str.split(self.ports_sep)
        df = df.where(pd.notnull(df), None)
        return dict(df.values)
