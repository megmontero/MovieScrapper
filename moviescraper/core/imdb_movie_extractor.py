"""
IMDBMovieExtractor
"""

from bs4 import BeautifulSoup 
import json
class IMDBMovieExtractor():
    def __init__(self, base_url):
        self._base_url = base_url
    
    def get_movie_info(self, movie_page):
        """
        Extracts all the movie info from a html movie page
        """
        # TODO: implement
        soup = BeautifulSoup(movie_page , "html.parser")

        title,year = (soup.select('h1')[0].text.strip()).split("\xa0")
        year = int(year.strip('()'))
        pageId = soup.find("meta",  property="pageId")["content"]

        data = json.loads(soup.find('script', type='application/ld+json').text)
        
        movie_info = {'title': title, "year": year, "id":pageId , "data": data}
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
