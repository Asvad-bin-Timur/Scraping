import pandas as pd
import requests as rq
from bs4 import BeautifulSoup as bs
import scrapy

url = 'https://www.kinopoisk.ru/lists/movies/top250/'
# TODO: make variables more explicit r -> request
r = rq.get(url).text
soup = bs(r, 'lxml')
soup.find('div', class_='styles_root__ti07r')
#captcha problem
