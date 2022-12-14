from scraper import KinoPoisk
from logger_info import logger
import pandas as pd

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
        
        film = 0
        links = all_links[0:2]
        for link in links:
            Parser.go_to_page(link)
            characteristics = Parser.film_characteristics()
            columns = list(d.keys())
            columns_of_film = []
            if d == {}:
                for ch in characteristics:
                    d[ch[0]] = [ch[1:2]]
            else:
                for ch in characteristics:    
                    d[ch[0]] = [d[ch[0]], ch[1:2]]
                    columns_of_film.append(ch[0])
            for column in columns:
                if column not in columns_of_film:
                    d[column] = [d[column], 'Null']
                else:
                    continue
            film += 1
            logger.info(f'Proccessed {film} films')
        df = pd.DataFrame(d)
        print(df)



if __name__ == '__main__':
    main()
