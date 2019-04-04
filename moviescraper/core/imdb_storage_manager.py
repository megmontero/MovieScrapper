"""
IMDBStorageManager
"""

from unqlite import UnQLite
class IMDBStorageManager():
    """
    Class for storing each movie
    """
    # TODO: complete, debug mode on
    def __init__(self, dbfile="db/imdb_dataset"):
        self._dbfile = dbfile
        self._db = UnQLite(self._dbfile)

    def write(self, movie, collection="movies"):
        col = self._db.collection(collection)
        col.create()
        col.store(movie)
        self._db.commit()
