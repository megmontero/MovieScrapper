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
        if search_result is None:
            return False
        return len(search_result) > 0

