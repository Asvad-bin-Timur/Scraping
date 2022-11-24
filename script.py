# TODO: make README file with project description
# TODO: look at logger library to use logs instead of prints
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class film_links:
    '''Класс для парсинга веб-страницы со списком фильмов в Кинопоиске'''
    links = []
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service)

    def __init__(self, url, class_name):
        self.url = url
        self.class_name = class_name 
    
    def make_a_list(self):
        self.driver.get(self.url)
        films = self.driver.find_elements(By.CLASS_NAME, self.class_name)
        for film in films:
            link = film.get_attribute('href')
            film_links.links.append(link)
        
    def show_links(self):
        print(film_links.links)

page1 = film_links('https://www.kinopoisk.ru/lists/movies/top250/', 'base-movie-main-info_link__YwtP1')
page1.make_a_list()
page1.show_links()