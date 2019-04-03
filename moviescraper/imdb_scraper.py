"""

IMDB Scraper class

Authors:
            Gregorio A. García Menéndez (gagarcia)
            Manuel E. Gómez Montero

"""

from core.imdb_agent_generator import IMDBAgentGenerator
from core.imdb_movie_extractor import IMDBMovieExtractor
from core.imdb_crawler import IMDBCrawler
from core.imdb_storage_manager import IMDBStorageManager
import datetime

class IMDBScraper():
    """
    IMDBScraper class
    """
    def __init__(self, **kwargs):
        
        self._base_url = 'https://www.imdb.com'
        self._endpoint = '/search/title?title_type=feature&year='
        self._user_agent_generator = IMDBAgentGenerator()
        self._archiver = IMDBStorageManager()
        self._extractor = IMDBMovieExtractor(self._base_url)
        self._crawler = IMDBCrawler(self._base_url)
        
    def _get_movies(self, endpoint):
        url = self._base_url + endpoint
        # TODO: Complete implementation
        next_page_url = url
        while next_page_url is not None:
            list_page = self._crawler.get_movie_list_page(next_page_url)
            movie_list, next_page_url = self._extractor.get_movie_list(list_page)
            for movie_url in movie_list:
                movie_page = self._crawler.get_movie_page(movie_url)
                movie_info = self._extractor.get_movie_info(movie_page)
                # STUB!!! DEBUG!! UNCOMMENT!!
                # self._archiver.write(movie_info)
                self._archiver.write(movie_url)

    def _get_movies_full(self):
        """
        Retrieve all movies in IMDB, full query
        """
        # TODO: Change last date for current day!
        end_date = datetime.datetime.today().strftime('%Y-%m-%d')
        endpoint = '/search/title?title_type=feature&year=1894-01-01' + ',' + end_date
        self._get_movies(endpoint)
        
    def _get_movies_year(self, int):
        """
        Retrieve all movies in IMDB for the given year
        """
        endpoint = '/year/' + str(int)
        self._get_movies(endpoint)
        
    def run(self):
        # TODO: get arguments?
        # if mode=='full':
        #   self.get_movies_full()
        # elif ...
        self._get_movies_full()

scraper = IMDBScraper()
scraper.run()     