"""
IMDBCrawler
"""
import requests
import random
import time
from .imdb_agent_generator import IMDBAgentGenerator

class IMDBCrawler():
    """
    IMDBCrawler class
    """

    def __init__(self, url, movie_endpoint, movie_rating_endpoint, person_endpoint):

        self._base_url = url
        self._sleep_min = 1
        self._sleep_max = 2
        self._user_agent_generator = IMDBAgentGenerator()
        self._movie_endpoint = movie_endpoint
        self._movie_rating_endpoint = movie_rating_endpoint 
        self._person_endpoint = person_endpoint
        
    def _get_agent(self):
        """
        Generates a new user agent to be user
        """
        return self._user_agent_generator.random_agent()
    
    def _sleep(self):
        """
        Sleeps random seconds so we don't get banned :)
        """
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
