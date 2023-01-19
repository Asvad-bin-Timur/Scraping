from scraper import KinoPoisk
from logger_info import logger
import pandas as pd
import sqlite3 as sql
from Data_processing import DataTransformation
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

def _budget(transformer: DataTransformation, x):
    currencies_signs = ['€', 'DEM', 'р.', '₽', '£', 'FRF', '¥', 'DKK']
    currencies = ['EUR', 'DEM', 'RUB', 'RUB', 'GBP', 'FRF', 'JPY', 'DKK']
    try:
        year = transformer.df_cleared.loc[transformer.df_cleared['Бюджет'] == x, 'Год производства'].values[0]
        for currency in currencies_signs:
            if currency in str(x):
                print(x)
                x = transformer.replace_symbol_of_cell(cell=x, symbol_to_be_replaced=currency, replacement='')
                print(x)
                x = float(x)
                x = transformer.convert_to_currency(cell=x, currency=currencies[currencies_signs.index(currency)],year = date(year, 1, 1))
            else:
                continue
        return x
    except:
        return x

def budget_column(transformer: DataTransformation):
    garbage = [' ', '$']
    for element in garbage:
        transformer.clear_column(column='Бюджет', replacement='', to_be_replaced=element)   
    transformer.df_cleared['Бюджет'] = transformer.df_cleared['Бюджет'].apply(lambda y: _budget(transformer, x=y))
    transformer.df_cleared['Бюджет'] = transformer.df_cleared['Бюджет'].apply(pd.to_numeric)
    return transformer.df_cleared
    

def categorical_columns(transformer: DataTransformation):
    columns = ['Жанр', 'Страна', 'Актеры', 'Режиссер', 'Сценарий']
    for column in columns:
        transformer.categorical_data_processing(column=column)
    return transformer.df_cleared
    

def views_column(transformer: DataTransformation):
    transformer.df_cleared['Зрители'] = transformer.df_cleared['Зрители'].apply(lambda x: transformer.convert_to_float(cell=x))
    return transformer.df_cleared

def fees_columns(transformer: DataTransformation):
    columns = ['Сборы в США', 'Сборы в мире']
    garbage = [' ', '$']    
    for column in columns:
        for element in garbage:
            transformer.clear_column(column=column, replacement='', to_be_replaced=element)
        transformer.df_cleared[column] = transformer.df_cleared[column].apply(lambda x: max(x.split('=')) if type(x) == str else x) 
    return transformer.df_cleared
        
def create_db_table(df):
    sqlite_file = 'KinoPoisk.db'
    table_name = 'films_data'
    conn = sql.connect(sqlite_file)
    df.to_sql(table_name, con=conn)
    conn.commit()
    conn.close()

def main():
    with KinoPoisk() as parser:
        all_links = find_links(parser)
        all_film_data = find_all_film_data(parser, all_links)
        df = pd.DataFrame(all_film_data)

    transformer = DataTransformation(df)
    transformer.dropping_columns()
    budget_column(transformer)
    categorical_columns(transformer)
    views_column(transformer)
    df = fees_columns(transformer)
    df.to_csv('KinoPoisk_processed', index=False)
    create_db_table(df=df)

if __name__ == '__main__':
    main()
