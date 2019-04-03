"""
IMDBStorageManager
"""

from unqlite import UnQLite
class IMDBStorageManager():
    """
    Class for storing each movie
    """
    # TODO: complete, debug mode on
    def __init__(self):
        pass
        
    def write(self, movie, dbfile="db/imdb_dataset", collection="movies"):
        db = UnQLite(dbfile)
        col = db.collection(collection)
        col.create()
        col.store(movie)
        db.commit()
