from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class KinoPoisk(webdriver.Chrome):
    """Class is used for parsing and analysing data from Kinopoisk website

    Args:
        webdriver (_type_): _description_

    Methods:
    go_to_page()
        Method to go to the website
    find_film_links()
        Method to get url links to single movie
    film_characteristics()
        Method to get data to single movie

    """
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
        self.quit()

    def go_to_page(self, url: str):
        """Method to go to the web page through url

        Args:
            url (_type_): _description_
        """
        self.get(url)

    def find_film_links(self, class_name: str = 'base-movie-main-info_link__YwtP1') -> list[str]:
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

    def film_characteristics(self, class_name_characteristics: str ='styles_row__da_RK', class_name_title: str='styles_title__hTCAr') -> list[list]:
        """Method to get data to single movie from top 250 list of movies

        Args:
            class_name_characteristics (str, optional): _description_. Defaults to 'styles_row__da_RK'.
            class_name_title (str, optional): _description_. Defaults to 'styles_rootInDark__SZlor'.

        Returns:
            _type_: _description_
        """
        characteristics = self.find_elements(By.CLASS_NAME, class_name_characteristics)
        characteristics_text = []
        film_name = self.find_element(By.CLASS_NAME, class_name_title).text
        characteristics_text.append(['Название фильма',film_name.split("\n")])
        for characteristic in characteristics:
            ch = characteristic.text.split("\n")
            if '4K доступно только на больших экранах' in ch or 'Качество видео' in ch:
                continue
            else:
                characteristics_text.append(ch)
        return characteristics_text
