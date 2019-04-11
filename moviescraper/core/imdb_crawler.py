"""
IMDBCrawler
"""
import requests
import random
import time
from .imdb_agent_generator import IMDBAgentGenerator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class IMDBCrawler():
    """
    IMDBCrawler class
    """

    def __init__(self, url, movie_endpoint, movie_rating_endpoint, person_endpoint, 
                movie_reviews_endpoint, user_endpoint):

        self._base_url = url
        self._sleep_min = 1
        self._sleep_max = 2
        self._request_per_second = 5 # Set to 1 or less if you want to do 1 or less request per second 
        self._user_agent_generator = IMDBAgentGenerator()
        self._movie_endpoint = movie_endpoint
        self._movie_rating_endpoint = movie_rating_endpoint 
        self._person_endpoint = person_endpoint
        self._movie_reviews_endpoint = movie_reviews_endpoint 
        
        CHROME_PATH = '/usr/bin/google-chrome-stable'
        CHROMEDRIVER_PATH = 'drivers/chromedriver'
        WINDOW_SIZE = "1920,1080"

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.binary_location = CHROME_PATH

        self._driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                          chrome_options=chrome_options
                         )
       
        
        
    def _get_agent(self):
        """
        Generates a new user agent to be user
        """
        return self._user_agent_generator.random_agent()
    
    def _sleep(self):
        """
        Sleeps random seconds so we don't get banned :)
        """
        if self._request_per_second > 1:
            if random.randint(0, self._request_per_second)%self._request_per_second == 0:
                time.sleep(1)
            return
        seconds = random.randint(self._sleep_min, self._sleep_max)
        time.sleep(seconds)
    
    def _http_get(self, url):
        """
        HTTP GET envelope
        """
        user_agent = self._get_agent()
        headers = {'User-Agent': user_agent}
        self._sleep()
        request_result = requests.get(url, headers=headers)
        status_code = request_result.status_code
        if status_code >= 400:
            return None
        return request_result.text

    def _http_get_infinite_scroll(self, url, load_class):
        """
        GET HTML Page with infinite scroll with selenium
        """
        self._sleep()
        self._driver.get(url)
        html = self._driver.page_source.encode('utf-8')
        page_num = 0
        while self._driver.find_elements_by_class_name(load_class):
            self._sleep()
            try:
                self._driver.find_elements_by_class_name(load_class)[0].click()
            except: 
                return (html, page_num)
                
            page_num += 1
        html = self._driver.page_source.encode('utf-8')
        return (html, page_num)
        
    
    def get_movie_page(self, movie_id):
        page = self._http_get(self._base_url + self._movie_endpoint.format(movie_id))
        return page

    def get_movie_rating_page(self, movie_id):
        page = self._http_get(self._base_url + self._movie_rating_endpoint.format(movie_id))
        return page
        
    def get_movie_list_page(self, url):
        page = self._http_get(url)
        return page

    def get_person_page(self, person_id):
        page = self._http_get(self._base_url + self._person_endpoint.format(person_id))
        return page

    def get_movie_reviews_page(self, movie_id):
        url = self._base_url + self._movie_reviews_endpoint.format(movie_id)
        html, _ =  self._http_get_infinite_scroll(url, "load-more-data")
        return html
    
    def get_user_page(self, url):
        page = self._http_get(url)
        return page

