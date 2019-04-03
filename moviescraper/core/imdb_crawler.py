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

    def __init__(self, url):

        self._base_url = url
        self._sleep_min = 1
        self._sleep_max = 2
        self._user_agent_generator = IMDBAgentGenerator()
        
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
        return requests.get(url, headers=headers)
    
    def get_movie_page(self, url):
        # TODO: get movie page
        page = self._http_get(url).text
        return page
        
    def get_movie_list_page(self, url):
        # TODO: get the list movie page
        page = self._http_get(url).text
        return page