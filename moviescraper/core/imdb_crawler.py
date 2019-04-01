"""
IMDBCrawler
"""
import requests


class IMDBCrawler():
	"""
    IMDBCrawler class
	"""

	def __init__(self, url):

        self._base_url = url
        
    def _get_agent(self):
        """
        Generates a new user agent to be user
        """
        return self._user_agent_generator.random
    
    def _sleep(self):
        """
        Sleeps random seconds so we don't get banned :)
        """
        seconds = random.randint(self.sleep_min, self.sleep_max)
        time.sleep(seconds)
    
    def _http_get(self, url):
        """
        HTTP GET envelope
        """
        user_agent = self._get_agent()
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'User-Agent': user_agent}
        self._sleep()
        requests.get(url, headers=headers)
    
    def get_movie_page(self, url):
        # TODO: get movie page
        pass
        
    def get_movie_list_page(self, url):
        # TODO: get the list movie page
        pass