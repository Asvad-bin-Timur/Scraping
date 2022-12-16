from scraper import KinoPoisk
from logger_info import logger
import pandas as pd
from selenium.webdriver.common.by import By


def main():
    with KinoPoisk() as Parser:
        all_links = []
        page = 1
        d = {}

        while True:
            url_of_page = Parser.base_url + str(page)
            Parser.go_to_page(url_of_page)
            logger.info(f'Went to page: {page}')
            links = Parser.find_film_links()
            logger.info(f'Parsed {len(links)} links')
            if links != []:
                all_links.extend(links)
                page += 1
                continue
            else:
                break
        logger.info(f'Total parsed links: {len(all_links)}')

        logger.info('Starting getting columns')
        all_columns = []
        link_number = 0
        for link in all_links:
            Parser.go_to_page(url=link)
            columns = Parser.find_elements(By.CLASS_NAME, 'styles_title__b1HVo')
            for column in columns:
                all_columns.append(column.text)
            link_number += 1
            logger.info(f'Processed {link_number} films columns')
        all_columns = list(set(all_columns))
        logger.info('All_columns is set')

        film = 0
        columns = {column: [] for column in all_columns}
        columns['Название фильма'] = []
        for link in all_links:
            Parser.go_to_page(link)
            characteristics = Parser.film_characteristics()
            film_data = {ch[0]: ch[1:2] for ch in characteristics}
            for column in list(columns.keys()):
                if column not in list(film_data.keys()):
                    film_data[column] = ['Null']
                else:
                    continue
            for row in film_data:
                if columns[row] == []:
                    columns[row] = film_data[row]
                else:
                    columns[row].extend(film_data[row])
            film += 1
            logger.info(f'Processed {film} films')
        df = pd.DataFrame(columns)
        df.to_csv('Kinopoisk.csv')


if __name__ == '__main__':
    main()
