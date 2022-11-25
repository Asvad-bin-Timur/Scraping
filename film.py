from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class KinoPoisk(webdriver.Chrome):
    def __init__(
        self,        
        base_url = 'https://www.kinopoisk.ru/lists/movies/top250/',
        teardown=False
    ):
        self.base_url = base_url
        self.teardown = teardown

        service = Service('/usr/bin/chromedriver')
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
        links = []
        for film in films:
            link = film.get_attribute('href')
            links.append(link)
        return links
    



with KinoPoisk() as Parser:
    Parser.go_to_page()
    links = Parser.find_film_links()
    print(links)

