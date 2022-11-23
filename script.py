import pandas as pd
import requests as rq
from bs4 import BeautifulSoup as bs
import scrapy

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from tqdm import tqdm 
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

s = Service('/usr/bin/chromedriver')
d = webdriver.Chrome(service=s)
d.get('https://www.kinopoisk.ru/lists/movies/top250/')
films = d.find_elements(By.CLASS_NAME,'base-movie-main-info_link__YwtP1')
links = []
for film in films:
    link = film.get_attribute('href')
    links.append(link)
print(links)





