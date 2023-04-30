import pandas as pd
from currency_converter import CurrencyConverter
from datetime import date


class DataTransformation():

    def __init__(
        self,
        df,
    ):
        self.df = df
        self.df_cleared = None

    def dropping_columns(self, thresh_number=170):
        self.df_cleared = self.df.dropna(axis=1, thresh=thresh_number)

    def replace_symbol_of_cell(self, cell, symbol_to_be_replaced, replacement):
        if type(cell) == str:
            cell = cell.replace(symbol_to_be_replaced, replacement)
        else:
            cell = str(cell)
            cell = cell.replace(symbol_to_be_replaced, replacement)
        return cell

    def convert_to_currency(self, cell, currency_input, year, currency_required='USD'):
        converter = CurrencyConverter()
        cell = (converter.convert(cell, currency_input,
                currency_required, date=date(year, 1, 1)))
        return cell

    def clear_column(self, column, replacement, to_be_replaced):
        self.df_cleared[column] = self.df_cleared[column].str.replace(
            to_be_replaced, replacement)

    def convert_to_float(self, cell):
        list_of_symbols = [' ', 'млн.', 'тыс.', 'млн', 'тыс', 'nan']
        list_of_replacements = ['', '000000', '000', '000000', '000', '0']
        if type(cell) != str:
            cell = str(cell)
        for symbol in list_of_symbols:
            if symbol in cell:
                cell = cell.replace(
                    symbol, list_of_replacements[list_of_symbols.index(symbol)])
        if '.' in cell:
            cell = cell.replace('.', '')
            cell = float(cell) * (0.1)
            return int(cell)
        else:
            return int(cell)

    def _budget(self, x):
        currencies_signs = ['€', 'DEM', 'р.', '₽', '£', 'FRF', '¥', 'DKK']
        currencies = ['EUR', 'DEM', 'RUB', 'RUB', 'GBP', 'FRF', 'JPY', 'DKK']
        try:
            year = self.df_cleared.loc[self.df_cleared['Бюджет']
                                       == x, 'Год производства'].values[0]
            for currency in currencies_signs:
                if currency in str(x):
                    x = self.replace_symbol_of_cell(
                        cell=x, symbol_to_be_replaced=currency, replacement='')
                    x = float(x)
                    x = self.convert_to_currency(
                        cell=x, currency_input=currencies[currencies_signs.index(currency)], year=date(year, 1, 1))
                else:
                    continue
            return x
        except ImportError:
            return x

    def budget_column(self):
        garbage = [' ', '$']
        for element in garbage:
            self.clear_column(column='Бюджет', replacement='',
                              to_be_replaced=element)
        self.df_cleared['Бюджет'] = self.df_cleared['Бюджет'].apply(
            lambda y: self._budget(y))
        self.df_cleared['Бюджет'] = self.df_cleared['Бюджет'].apply(
            pd.to_numeric)

    def views_column(self):
        self.df_cleared['Зрители'] = self.df_cleared['Зрители'].apply(
            lambda x: self.convert_to_float(x))

    def fees_columns(self):
        columns = ['Сборы в США', 'Сборы в мире']
        garbage = [' ', '$']
        for column in columns:
            for element in garbage:
                self.clear_column(column=column, replacement='',
                                  to_be_replaced=element)
        self.df_cleared['Сборы в мире'] = self.df_cleared['Сборы в мире'].apply(
            lambda x: max(x.split('=')) if type(x) == str else x)
