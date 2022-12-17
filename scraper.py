from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class KinoPoisk(webdriver.Chrome):
    """Class is used for parsing data from Kinopoisk website

    Args:
        webdriver: Chrome web driver

    Methods:
    go_to_page()
        Method to go to the website by given url
    find_film_links()
        Method to get url links to single movie
    film_characteristics()
        Method to get data from single movie

    """

    def __init__(
        self,
        base_url: str = 'https://www.kinopoisk.ru/lists/movies/top250/?page=',
        teardown: bool = False
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

    def go_to_page(self, url: str) -> None:
        """Method to go to the web page through url

        Args:
            url (str): Web address of page

        Returns:
            None:
        """
        self.get(url)

    def find_film_links(
        self,
        class_name: str = 'base-movie-main-info_link__YwtP1'
    ) -> list[str]:
        """Method to get url links to single movie from top 250 list of movies

        Args:
            class_name (str, optional): Name of movie class.
            Defaults to 'base-movie-main-info_link__YwtP1'.

        Returns:
            list[str]: List with urls of movies
        """
        films = self.find_elements(By.CLASS_NAME, class_name)
        links = []
        for film in films:
            link = film.get_attribute('href')
            links.append(link)

        return links

    def film_characteristics(
        self,
        class_name_characteristics: str = 'styles_row__da_RK',
        class_name_title: str = 'styles_title__hTCAr'
    ) -> list[list]:
        """Method to get data from single movie from top 250 list of movies

        Args:
            class_name_characteristics (str, optional): Name of the class of movie characteristics.
            Defaults to 'styles_row__da_RK'.
            class_name_title (str, optional): Name of thew class of movie name.
            Defaults to 'styles_rootInDark__SZlor'.

        Returns:
            list: List of lists of movie characteristics
        """

        characteristics_text = []

        film_name = self.find_element(By.CLASS_NAME, class_name_title).text
        characteristics_text.append(['Название фильма', film_name.split("\n")])
        characteristics = self.find_elements(
            By.CLASS_NAME, class_name_characteristics
        )
        for characteristic in characteristics:
            ch = characteristic.text.split("\n")
            if ch not in ('4K доступно только на больших экранах', 'Качество видео'):
                characteristics_text.append(ch)

        return characteristics_text

    def film_characteristics(
        self,
        class_name_characteristics: str = 'styles_row__da_RK',
        class_name_title: str = 'styles_title__hTCAr'
    ) -> dict[str, str]:
        """Method to get data from single movie from top 250 list of movies

        Args:
            class_name_characteristics (str, optional): Name of the class of movie characteristics.
            Defaults to 'styles_row__da_RK'.
            class_name_title (str, optional): Name of thew class of movie name.
            Defaults to 'styles_rootInDark__SZlor'.

        Returns:
            dict: Data dictionary for single movie
        """
        film_name = self.find_element(By.CLASS_NAME, class_name_title).text
        characteristics = self.find_elements(
            By.CLASS_NAME, class_name_characteristics
        )

        film_data = {ch[0]: ch[1:2] for ch in (characteristic.text.split("\n") for characteristic in characteristics) if ch not in (
            '4K доступно только на больших экранах', 'Качество видео'
        )}
        film_data['Название фильма'] = film_name.split("\n")

        return film_data
