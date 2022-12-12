from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd


class KinoPoisk(webdriver.Chrome):
    def __init__(
        self,        
        base_url = 'https://www.kinopoisk.ru/lists/movies/top250/?page=1',
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
    
    def go_to_page(self, url):
        self.get(url)
    
    def find_film_links(self, class_name= 'base-movie-main-info_link__YwtP1'):
        films = self.find_elements(By.CLASS_NAME,class_name)
        self.links = []
        for film in films:
            link = film.get_attribute('href')
            self.links.append(link)
        return self.links

    def find_all_links(self):
        all_links = []
        page = 0
        loop = True
        while loop == True:
            page = page + 1
            url_of_page = f'https://www.kinopoisk.ru/lists/movies/top250/?page={page}'
            self.go_to_page(url=url_of_page)
            links = self.find_film_links()
            if links != []:
                all_links = all_links + links
                continue
            else:
                loop = False
        return all_links 
            
    
    def film_characteristics(self):
            self.get('https://www.kinopoisk.ru/film/435/')
            characteristics = self.find_elements(By.CLASS_NAME,'styles_row__da_RK')
            characteristics_text = []
            for characteristic in characteristics:
                ch = characteristic.text.split("\n")
                characteristics_text.append(ch)
            return characteristics_text

with KinoPoisk() as Parser:
    all_links = Parser.find_all_links()
    print(len(all_links))



