from scraper import KinoPoisk
from logger_info import logger
import pandas as pd
import sqlite3 as sql
from Data_processing import data_transformation
from datetime import date



def find_links(parser: KinoPoisk) -> list[str]:

    all_links = []
    page = 1

    while True:
        url_of_page = parser.base_url + str(page)
        parser.go_to_page(url_of_page)
        logger.info(f'Went to page: {page}')
        links = parser.find_film_links()
        logger.info(f'Parsed {len(links)} links')
        if links != []:
            all_links.extend(links)
            page += 1
            continue
        else:
            break
    logger.info(f'Total parsed links: {len(all_links)}')

    return all_links

def find_all_film_data(parser: KinoPoisk, all_links: list) -> list[dict]:
    all_film_data = []
    for link_number, link in enumerate(all_links):
        parser.go_to_page(link)
        film_data = parser.film_characteristics()
        all_film_data.append(film_data)
        logger.info(f'Got data from the {link_number+1} link film')
    return all_film_data

def __budget__(transformer: data_transformation, x):
    currencies_signs = ['€', 'DEM', 'р.', '₽', '£', 'FRF', '¥', 'DKK']
    currencies = ['EUR', 'DEM', 'RUB', 'RUB', 'GBP', 'FRF', 'JPY', 'DKK']
    year = transformer.df_cleared.loc[transformer.df_cleared['Бюджет'] == x, 'Год производства'].values[0]
    for currency in currencies_signs:
        if type(x) == str:
            if currency in x:
                x = float(transformer.replace_symbol_of_cell(cell=x, symbol_to_be_replaced=currency, replacement=''))
                x = transformer.convert_to_usd(cell=x, currency=currencies[currencies_signs.index(currency)],year = date(year, 1, 1))
            else:
                continue
        elif type(x) != str:
            x = str(x)
            if currency in x:
                x = float(transformer.replace_symbol_of_cell(cell=x, symbol_to_be_replaced=currency, replacement=''))
                x = transformer.convert_to_usd(cell=x, currency=currencies[currencies_signs.index(currency)],year = date(year, 1, 1))
            else:
                continue
    return x

def budget_column(transformer: data_transformation):
    garbage = [' ', '$']    
    for element in garbage:
        transformer.clean_column(column='Бюджет', replacement='', to_be_replaced=element)
    transformer.df_cleared['Бюджет'] = transformer.df_cleared['Бюджет'].apply(lambda y: __budget__(x=y))
    transformer.df_cleared['Бюджет'] = transformer.df_cleared['Бюджет'].apply(pd.to_numeric)
    

def categorical_columns(transformer: data_transformation):
    columns = ['Жанр', 'Страна', 'Актеры', 'Режиссер', 'Сценарий']
    for column in columns:
        transformer.categorical_data_processing(column=column)
    

def views_column(transformer: data_transformation):
    transformer.df_cleared['Зрители'] = transformer.df_cleared['Зрители'].apply(lambda x: transformer.convert_to_float(cell=x))
    transformer.df_cleared.to_csv('KinoPoisk.csv')

def fees_columns(transformer: data_transformation):
    columns = ['Сборы в США', 'Сборы в мире']
    garbage = [' ', '$']    
    for column in columns:
        for element in garbage:
            transformer.clean_column(column=column, replacement='', to_be_replaced=element)
        transformer.clean_column(column=column, replacement=0, to_be_replaced='nan')
        transformer.df_cleared[column] = transformer.df_cleared[column].apply(lambda x: max(x.split('=')) if type(x) == str else x) 
        
def create_db_table():
    sqlite_file = 'KinoPoisk.db'
    table_name = 'films_data'
    conn = sql.connect(sqlite_file)
    pd.read_csv('KinoPoisk.csv').to_sql(table_name, con=conn)
    conn.commit()
    conn.close()

def main():
    '''with KinoPoisk() as parser:
        all_links = find_links(parser)
        all_film_data = find_all_film_data(parser, all_links)
        df = pd.DataFrame(all_film_data)
        df.to_csv('KinoPoisk.csv', index=False)'''

    with data_transformation() as transformer:
        data_transformation.dropping_columns(transformer)
        budget_column(transformer)
        categorical_columns(transformer)
        views_column(transformer)
        fees_columns(transformer)
        transformer.df_cleared.to_csv('KinoPoisk.csv')
        
    #create_db_table()

if __name__ == '__main__':
    main()
