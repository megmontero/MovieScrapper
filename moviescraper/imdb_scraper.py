"""

IMDB Scraper class

Authors:
            Gregorio A. García Menéndez (gagarcia)
            Manuel E. Gómez Montero

"""

from moviescraper.core.imdb_agent_generator import IMDBAgentGenerator
from moviescraper.core.imdb_movie_extractor import IMDBMovieExtractor
from moviescraper.core.imdb_crawler import IMDBCrawler
from moviescraper.core.imdb_storage_manager import IMDBStorageManager

        
class IMDBScraper():
	"""
    IMDBScraper class
	"""

	def __init__(self, **kwargs):
        
        self._dbmgr = IMDBDStorageManager()
        self._user_agent_generator = IMDBAgentGenerator()
        self._archiver = IMDBStorageManager()
        self._extractor = IMDBMovieExtractor()
        self._base_url = "https://www.imdb.com"
        self._endpoint = "/search/title?title_type=feature&year="
        
    def _get_movies(self, endpoint):
        url = self._base_url + endpoint
        # TODO: Complete implementation
        list_page = self._crawler.get_movie_list_page(url)
        movie_list = self._extractor.get_movie_list(list_page)
        for movie_url in movie_list:
            movie_page = self._crawler.get_movie_page(movie_url)
            movie_info = self._extractor.get_movie_info(movie_page)
            self._archiver.write(movie_info)
        
    def _get_movies_full(self):
        """
        Retrieve all movies in IMDB, full query
        """
        # TODO: Change last date for current day!
        endpoint = "/search/title?title_type=feature&year=" + '1894-01-01' + '2019-04-01'
        self._crawler = IMDBCrawler(endpoint)
        
    def _get_movies_year(self, int):
        """
        Retrieve all movies in IMDB for the given year
        """
        endpoint = "/year/" + str(int)
        self._crawler = IMDBCrawler(endpoint)
        
    def run(self):
        # TODO: get arguments?
        # if mode=='full':
        #   self.get_movies_full()
        # elif ...
        self.get_movies_full()

        