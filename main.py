from scraper import KinoPoisk
from logger_info import logger
import pandas as pd
import sqlite3 as sql
from Data_processing import DataTransformation


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
    transformer.budget_column()
    transformer.categorical_columns()
    transformer.views_column()
    transformer.fees_columns()
    transformer.df_cleared.to_csv('KinoPoisk_processed', index=False)
    create_db_table(df)


if __name__ == '__main__':
    main()
