from scraper import KinoPoisk
import pandas as pd
import numpy as np
from currency_converter import CurrencyConverter
from datetime import date
import numpy as np
import pandas as pd

# This script doesn't work for now

class DataTransformation():

    def __init__(self, 
                df):
        self.df = df

    def __enter__(self):
        print('Start data transformation')

    def __exit__(self, exc_type, exc_value, ex_traceback):
        print('End data transformation')
    
    def dropping_columns(self, thresh_number=180):
        self.df_cleared = self.df.dropna(axis=1, thresh=thresh_number)


    def replace_symbol_of_cell(self, cell, symbol_to_be_replaced, replacement):
        if type(cell) == str:
            self.cell = cell.replace(symbol_to_be_replaced, replacement)
        else:
            cell = str(cell)
            self.cell = cell.replace(symbol_to_be_replaced, replacement)
        return self.cell


    def convert_to_currency(self, cell, currency_input, year, currency_required='USD'):
        converter = CurrencyConverter()
        self.cell = (converter.convert(cell, currency_input, currency_required, date=date(year, 1, 1)))

    def clear_column(self, column, replacement, to_be_replaced):
        self.df_cleared[column] = self.df_cleared[column].str.replace(to_be_replaced, replacement)

    def convert_to_float(self, cell):
        list_of_symbols = [' ', 'млн.', 'тыс.', 'млн', 'тыс', 'nan']
        list_of_replacements = ['', '000000', '000', '000000', '000', '0']
        if type(cell) != str:
            cell = str(cell)
        for symbol in list_of_symbols:
            if symbol in cell:
                cell = cell.replace(symbol, list_of_replacements[list_of_symbols.index(symbol)])
        if '.' in cell:
            cell = cell.replace('.', '')
            cell = float(cell) * (0.1)
            return int(cell)
        else:
            return int(cell)

    def categorical_data_processing(self, column):
        all_categories = []
        for record in self.df_cleared[column]:
            new_record = record.split(',')
            for word in new_record:
                word = word.strip()
            all_categories.append(word)
        all_categories = list(set(all_categories))
        for category in all_categories:
            self.df_cleared[column + ': ' + category] = self.df_cleared[column].apply(
                lambda x: True if category in x else False)
