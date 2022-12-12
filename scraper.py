from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class KinoPoisk(webdriver.Chrome):
    def __init__(
        self,
        base_url='https://www.kinopoisk.ru/lists/movies/top250/?page=',
        teardown=False
    ):
        self.base_url = base_url
        self.teardown = teardown

        service = Service(executable_path='/usr/bin/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        caps = webdriver.DesiredCapabilities.CHROME.copy()
        caps['acceptInsecureCerts'] = True

        super(KinoPoisk, self).__init__(
            service=service,
            options=options,
            desired_capabilities=caps
        )
        self.implicitly_wait(15)
        self.maximize_window()

    def __enter__(self):
        print('Start Parsing')
        return self

    def __exit__(self, exc_type, exc_value, ex_traceback):
        print('End Parsing')

    def go_to_page(self, url):
        self.get(url)

    def find_film_links(self, class_name: str='base-movie-main-info_link__YwtP1') -> list[str]:
        """Method to get url links to single movie from top 250 list of movies

        Args:
            class_name (str, optional): _description_. Defaults to 'base-movie-main-info_link__YwtP1'.

        Returns:
            list[str]: _description_
        """
        films = self.find_elements(By.CLASS_NAME, class_name)
        links = []
        for film in films:
            link = film.get_attribute('href')
            links.append(link)
        return links

    def film_characteristics(self):
        self.go_to_page('https://www.kinopoisk.ru/film/435/')
        characteristics = self.find_elements(
            By.CLASS_NAME, 'styles_row__da_RK'
        )
        characteristics_text = []
        for characteristic in characteristics:
            ch = characteristic.text.split("\n")
            characteristics_text.append(ch)
        return characteristics_text
