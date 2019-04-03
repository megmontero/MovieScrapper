"""
IMDBMovieExtractor
"""

from bs4 import BeautifulSoup

class IMDBMovieExtractor():
    def __init__(self, base_url):
        self._base_url = base_url
    
    def get_movie_info(self, movie_page):
        """
        Extracts all the movie info from a html movie page
        """
        # TODO: implement
        movie_info = {'test': movie_page}
        return movie_info
    
    def get_movie_list(self, list_page):
        """
        Extracts all the movies url inside list_page
        """
        # TODO: implement next page url!!!
        movie_urls = []
        soup = BeautifulSoup(list_page, 'html.parser')
        movie_frames = soup.find_all(class_='lister-item-header')
        for frame in movie_frames:
            link = frame.find('a').get('href')
            movie_url = self._base_url + link
            movie_urls.append(movie_url)
        return (movie_urls, None)