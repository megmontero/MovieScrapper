"""
ImDBmovieExtractor
"""

from bs4 import BeautifulSoup 
import json
import re
class IMDBMovieExtractor():
    def __init__(self, base_url):
        self._base_url = base_url
    
    def get_movie_info(self, movie_page, movie_rating_page, movie_reviews_page):
        """
        Extracts all the movie info from a html movie page
        """
        soup = BeautifulSoup(movie_page , "html.parser")
        
        movie_info = json.loads(soup.find('script', type='application/ld+json').text)
        titleyear = (soup.select('h1')[0].text.strip()).split("\xa0")
        movie_info["title"] = movie_info["name"]#titleyear[0] Spanish title
        if len(titleyear)>1:
            movie_info["year"] = int(titleyear[1].strip('()'))
        movie_info["id"]= soup.find("meta",  property="pageId")["content"]

        if "actor" in movie_info:
            movie_info["actors"] = self.extract_person_list(movie_info["actor"])
        if "creator" in movie_info:
            movie_info["creators"] = self.extract_person_list(movie_info["creator"])
        if "director" in movie_info:
            movie_info["directors"] = self.extract_person_list(movie_info["director"])
        
        remove_keys = ["@context", "image", "url", "aggregateRating", 
                       "review", "trailer", "actor", "creator", "director", "name"]
        for k in remove_keys:
            movie_info.pop(k, None)
        movie_info["rating"]=  self._get_movie_rating_info(movie_rating_page)
        # STUB!!
        movie_info["reviews"] = self._get_movie_reviews_info(movie_reviews_page)

        return movie_info
   

    def extract_person_list(self,main_list):
        """
        From a list of creators, directors or actors extract only persons
        and change url for id
        """
        if not isinstance(main_list, list):
            main_list = [main_list]
        person_list = []
        for p in main_list:
            if p["@type"] == 'Person':
                new_person = {"name": p["name"],
                              "id": re.search("nm\d{7}", p["url"]).group(0)}
                person_list.append(new_person)
        return person_list 



    def get_movie_list(self, list_page):
        """
        Extracts all the movies url inside list_page
        """
        movie_ids = []
        soup = BeautifulSoup(list_page, 'html.parser')
        movie_frames = soup.find_all(class_='lister-item-header')
        next_page = soup.find("a", {"class":"next-page" }, href=True)
        if (next_page):
            next_page= self._base_url + next_page["href"]
        for frame in movie_frames:
            link = frame.find('a').get('href')
            movie_id = re.search("tt\d{7}", link).group(0)
            movie_ids.append(movie_id)
        return (movie_ids, next_page)

    def get_total_movies(self, list_page):
        """
        Extracts the total number of movies of the page
        """
        soup = BeautifulSoup(list_page, 'html.parser')
        page_desc = soup.find_all(class_='desc')[0]
        # text is in the format "1-50 of 11,250 titles."
        total_text = (page_desc.find('span').text).split()[2].replace(',', '')
        total_number = int(total_text)
        return total_number

    def _get_movie_reviews_info(self, movie_reviews_page):
        """
        Extracts movie reviews info from a html movie reviews page
        """
        reviews = [] 
        soup = BeautifulSoup(movie_reviews_page, 'html.parser')
        #user_info = soup.find_all(class_='display-name-link')
        #rating_info = soup.find_all(class_='rating-other-user-rating')
        rating_info = soup.find_all(class_='review-container')
        for rating in rating_info: 
           u = rating.find(class_='display-name-link').find("a", href=True)
           r_soup = soup.find(class_='rating-other-user-rating')
           if r_soup:
                new_rating = {"user": {"name": u.text , 
                                       "id":   re.search("ur\d{7}", u["href"]).group(0) },
                              "rating": float(r_soup.find("span").text)}
                reviews.append(new_rating)



        #for c, user in enumerate(user_info):
        #    u = user.find("a", href=True)
        #    new_rating = {"user": {"name": u.text , 
        #                           "id":   re.search("ur\d{7}", u["href"]).group(0) },
        #                  "rating": rating_info[c].find("span").text}
        #     reviews.append(new_rating)
        return reviews 

    def _get_movie_rating_info(self, movie_rating_page):
        """
        Extracts demographic rating info from a html movie rating page
        """
        soup = BeautifulSoup(movie_rating_page , "html.parser")
        movie_ratings = []
        rating_cells = soup.findAll("td", {"class": "ratingTable"})
        demo_labels = ["all", "<18", "18-29", "30-44", "45+", 
                        "males", "m<18", "m18-29", "m30-44", "m45+",
                        "females", "f<18", "f18-29", "f30-44", "f45+"]
        for c, label in enumerate(demo_labels):
            try:
                rating = float(rating_cells[c].find("div", {"class": "bigcell"}).text.strip())
                votes = int(rating_cells[c].find("div", {"class": "smallcell"}).text.replace(",", "").strip())
            except:
                rating = '-'
                votes = '-'
            group = {"group": label, "rating": rating, "votes": votes}
            movie_ratings.append(group)
        return movie_ratings

    def get_person_info(self, person_page):
        """
        Extracts info of the casting person page passed by parameter
        """
        soup = BeautifulSoup(person_page , "html.parser")
        movie_ratings = []
        casting_categories = soup.findAll("div", {"class": "head"})
        casting_section = soup.findAll("div", {"class": "filmo-category-section"})
        script_person_info = json.loads(soup.find('script', type='application/ld+json').text)
        person_info = {}
        person_info["id"] = soup.find("meta",  property="pageId")["content"]
        person_info["name"] = script_person_info["name"]
        try:
            # Optional field
            person_info["birth_date"] = script_person_info["birthDate"]
        except KeyError:
            person_info["birth_date"] = None

        casting_result = []
        for category, section in zip(casting_categories, casting_section):
            current_category = category.find("a").text
            item_list = []
            section_casting_odd = section.findAll("div", {"class": "filmo-row odd"})
            section_casting_even = section.findAll("div", {"class": "filmo-row even"})
            section_casting = section_casting_odd + section_casting_even
            for item in section_casting:
                current_item = {}
                current_id = item.get('id')
                item_id = current_id.split('-')[1]
                item_name = item.find("a").text
                current_item = {'name': item_name, 'id': item_id}
                item_list.append(current_item)
            person_info[current_category] = item_list

        return person_info

    def get_user_info(self, user_page):
        """
        Extracts info of the user from user page passed by parameter
        """
        user_info = {} 
        user_info["ratings"] = []
        soup = BeautifulSoup(user_page , "html.parser")
        user_info["id"] = soup.find("div", {"id": "main"})["data-userid"]
        header = soup.find("h1", {"class": "header"}).text
        user_info["name"] = header.split("'")[0]
        return user_info

    def get_user_ratings(self, user_page):
        """
        Extracts info of the rating from user page passed by parameter
        """
        user_ratings =  []
        soup = BeautifulSoup(user_page , "html.parser")
        
        items = soup.findAll("div", {"class":"lister-item"})
        for it in items:
            starts = it.findAll("span", {"class": "ipl-rating-star__rating"})
            movie = it.find("a", href=True)
            rate = {"global": float(starts[0].text),
                "rate": int(starts[1].text),
                "movie":{ "id": re.search("tt\d{7}", movie["href"]).group(0),
                    "title": movie.text}
                }
            user_ratings.append(rate)

        next_page = None

        return user_ratings, next_page

    def get_user_info(self, user_page):
        """
        Extracts info of the user from user page passed by parameter
        """
        user_info = {} 
        user_info["ratings"] = []
        soup = BeautifulSoup(user_page , "html.parser")
        user_info["id"] = soup.find("div", {"id": "main"})["data-userid"]
        header = soup.find("h1", {"class": "header"}).text
        user_info["name"] = header.split("'")[0]
        return user_info

    def get_user_ratings(self, user_page):
        """
        Extracts info of the rating from user page passed by parameter
        """
        user_ratings =  []
        soup = BeautifulSoup(user_page , "html.parser")
        
        items = soup.findAll("div", {"class":"lister-item"})
        for it in items:
            starts = it.findAll("span", {"class": "ipl-rating-star__rating"})
            movie = it.find("a", href=True)
            rate = {"global": float(starts[0].text),
                "rate": int(starts[1].text),
                "movie":{ "id": re.search("tt\d{7}", movie["href"]).group(0),
                    "title": movie.find("img")["alt"]}
                }
            break
            user_ratings.append(rate)

        next_page = None

        return user_ratings, next_page


