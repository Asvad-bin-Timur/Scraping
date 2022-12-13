from scraper import KinoPoisk
from logger_info import logger


def main():
    with KinoPoisk() as Parser:
        all_links = []
        page = 1

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

if __name__ == '__main__':
    main()
