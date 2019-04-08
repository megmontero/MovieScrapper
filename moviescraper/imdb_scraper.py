"""

IMDB Scraper class

Authors:
            Gregorio A. García Menéndez (gagarcia)
            Manuel E. Gómez Montero (mnlgmontero)

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
        self._movie_rating_endpoint = '/title/{}/ratings'
        self._movie_reviews_endpoint = '/title/{}/reviews'
        self._movie_endpoint = '/title/{}'
        self._person_endpoint = '/name/{}/?nmdp=1&ref_=nm_flmg_shw_1#filmography'
        self._user_agent_generator = IMDBAgentGenerator()
        self._archiver = IMDBStorageManager()
        self._extractor = IMDBMovieExtractor(self._base_url)

        self._crawler = IMDBCrawler(self._base_url,self._movie_endpoint,self._movie_rating_endpoint,
                                    self._person_endpoint, self._movie_reviews_endpoint)
        
    def _get_movies(self, endpoint):
        url = self._base_url + endpoint
        # TODO: Complete implementation
        next_page_url = url
        while next_page_url is not None:
            list_page = self._crawler.get_movie_list_page(next_page_url)
            movie_list, next_page_url = self._extractor.get_movie_list(list_page)
            for movie_id in movie_list:
                movie_page = self._crawler.get_movie_page(movie_id)
                rating_movie_page = self._crawler.get_movie_rating_page(movie_id)

                reviews_page = self._crawler.get_movie_reviews_page(movie_id)
                movie_info = self._extractor.get_movie_info(movie_page, rating_movie_page, reviews_page)
                # Iterate over all actors / creators / directors
                try:
                    actors_list = movie_info['actors']
                except KeyError:
                    actors_list = []
                try:
                    creators_list = movie_info['creators']
                except KeyError:
                    creators_list = []
                try:
                    directors_list = movie_info['directors']
                except KeyError:
                    directors_list = []
                for actor in actors_list:
                    actor_id = actor['id']
                    if not self._archiver.exists_id(actor_id, collection='persons'):
                        actor_page = self._crawler.get_person_page(actor_id)
                        if actor_page is not None:
                            actor_info = self._extractor.get_person_info(actor_page)
                            self._archiver.write(actor_info, collection='persons')
                for creator in creators_list:
                    creator_id = creator['id']
                    if not self._archiver.exists_id(creator_id, collection='persons'):
                        creator_page = self._crawler.get_person_page(creator_id)
                        if creator_page is not None:
                            creator_info = self._extractor.get_person_info(creator_page)
                            self._archiver.write(creator_info, collection='persons')
                for director in directors_list:
                    director_id = director['id']
                    if not self._archiver.exists_id(director_id, collection='persons'):
                        director_page = self._crawler.get_person_page(director_id)
                        if director_page is not None:
                            director_info = self._extractor.get_person_info(director_page)
                            self._archiver.write(director_info, collection='persons')

                # STUB!!! DEBUG!! UNCOMMENT!!
                self._archiver.write(movie_info)
                #self._archiver.write(movie_url)

    def _get_movies_full(self):
        """
        Retrieve all movies in IMDB, full query
        """
        # TODO: Change last date for current day!
        end_date = datetime.datetime.today().strftime('%Y-%m-%d')
        endpoint = '/search/title?title_type=feature&year=1894-01-01' + ',' + end_date
        ## DEBUG less time to test better

        endpoint = '/search/title?title_type=feature&year=2019-04-05' + ',' + end_date
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
