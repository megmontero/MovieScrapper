"""
IMDBStorageManager
"""

from unqlite import UnQLite
class IMDBStorageManager():
    """
    Class for storing each movie
    """
    def __init__(self, dbfile="db/imdb_dataset"):
        self._dbfile = dbfile
        self._db = UnQLite(self._dbfile)

    def write(self, doc, collection="movies"):
        if doc is not None:
            col = self._db.collection(collection)
            col.create()
            col.store(doc)
            self._db.commit()

    """
    Check if ID exists
    """
    def exists_id(self, docId, collection="movies"):
        col = self._db.collection(collection)
        if col is None:
            return False
        search_result = col.filter(lambda x: x["id"] == str.encode(docId))
        if not search_result:
            return False
        return len(search_result) > 0

    """
    Check if user has rated a movie
    """
    def is_movie_rated(self, movie_info, user_id):
        col = self._db.collection("users")
        if col is None:
            return False
        search_result = col.filter(lambda x: x["id"] == str.encode(user_id))
        if not search_result:
            return False
        for r in search_result[0]["ratings"]:
            if (r["movie"]["id"] == movie_info["id"]):
                return True
        return False


    """
    Add movie rate to user - create user if not exist
    """
    def add_user_rate(self, movie_info, user_id):
        col = self._db.collection("users")
        if col is None:
            return 
        search_result = col.filter(lambda x: x["id"] == str.encode(user_id))
        for dr in movie_info["rating"]:
           if dr["group"] == "all":
               global_rate = dr["rating"]
               break

        for r in movie_info["reviews"]:
           if(r["user"]["id"] == user_id):
               rate = r["rating"] 
               name = r["user"]["name"]
               break
        new_rate = {'global': global_rate,
                    'rate': rate,
                    'movie': { 'id': movie_info["id"],
                    'title':movie_info["title"]}}
        if not search_result:
           ##user not exist
           user_info = {"id": user_id,
                        "name": name,
                        "ratings": [new_rate]
                   }
           self.write(user_info, collection="users")
           return
        user = search_result[0]
        user["ratings"].append(new_rate)
        col.update(user["__id"], user)
        self._db.commit()

