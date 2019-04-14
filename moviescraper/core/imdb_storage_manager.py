"""
IMDBStorageManager
"""
from unqlite import UnQLite


CSV = True


class IMDBStorageManager():
    """
    Class for storing each movie
    """
    def __init__(self, dbfile="db/imdb_dataset"):
        self._dbfile = dbfile
        self._db = UnQLite(self._dbfile)
        self._movie_keys = ["id", "@type", "year", "title", "genre",
                            "contentRating", "description",
                            "datePublished", "keywords", "duration",
                            "rtng_all_v", "rtng_all_r", "rtng_<18_v",
                            "rtng_<18_r", "rtng_18-29_v", "rtng_18-29_r",
                            "rtng_30-44_v", "rtng_30-44_r", "rtng_45+_v",
                            "rtng_45+_r", "rtng_males_v", "rtng_males_r",
                            "rtng_m<18_v", "rtng_m<18_r", "rtng_m18-29_v",
                            "rtng_m18-29_r", "rtng_m30-44_v", "rtng_m30-44_r",
                            "rtng_m45+_v", "rtng_m45+_r", "rtng_females_v",
                            "rtng_females_r", "rtng_f<18_v", "rtng_f<18_r",
                            "rtng_f18-29_v", "rtng_f18-29_r", "rtng_f30-44_v",
                            "rtng_f30-44_r", "rtng_f45+_v", "rtng_f45+_r"]
        self._user_keys = ["id", "name"]
        self._person_keys = ["id", "name", "birth_date"]
        self._person_movie_key = ["id_person", "id_movie", "rol"]
        self._user_movie_key = ["id_user", "id_movie", "global", "rate"]
        self._rating_groups = ["all", ]
        self._write_csv_headers()

    def write(self, doc, collection="movies"):
        if doc is not None:
            col = self._db.collection(collection)
            col.create()
            col.store(doc)
            self._db.commit()
        if CSV:
            switcher = {
                "users": self._user_keys,
                "movies": self._movie_keys,
                "persons": self._person_keys
            }
            keys = switcher.get(collection, lambda: None)
            self._write_collection_csv(doc, collection, keys)

    def _write_csv_headers(self):
        """
        Write headers in csv files
        """
        csv_files_headears = {"persons.csv": self._person_keys,
                              "movies.csv": self._movie_keys,
                              "users.csv": self._user_keys,
                              "user_movie.csv": self._user_movie_key,
                              "person_movie.csv": self._person_movie_key}
        for f in csv_files_headears.keys():
            self._write_csv_row(f, csv_files_headears[f], mode="w")

    def _write_csv_row(self, file_name, row, mode="a"):
        """
        Write row on csv
        """
        f = open("dataset/" + file_name, mode)
        format_row = [('"' + r + '"') if isinstance(r, str)
                      else str(r) for r in row]
        f.write(";".join(format_row) + "\n")
        f.close()

    def _write_user_movie_csv(self, doc):
        """
        write relationship between user and movie
        """

        for r in doc["ratings"]:
            row = [doc["id"], r["movie"]["id"], r["global"], r["rate"]]
            self._write_csv_row("user_movie.csv", row)

    def _write_person_movie_csv(self, doc):
        """
        write relationship between person and movie
        """
        for k in doc.keys():
            if isinstance(doc[k], list):
                for movie in doc[k]:
                    row = [doc["id"], movie["id"], k]
                    self._write_csv_row("person_movie.csv", row)

    def _write_collection_csv(self, doc, collection, keys):
        """
        Write a collection row on csv
        """
        row = []
        file_name = collection + ".csv"
        for k in keys:
            # movie rating is more complex
            if "rtng_" in k:
                _, group_key, r_type = k.split("_")
                try:
                    for rate in doc["rating"]:
                        if rate["group"] == group_key:
                            if r_type == "v":
                                field = rate["votes"]
                            else:
                                field = rate["rating"]
                            break
                except Exception:
                    field = ""
            else:
                try:
                    if isinstance(doc[k], list):
                        field = ",".join(doc[k])
                    else:
                        field = doc[k]
                except Exception:
                    field = ""
            row.append(field)
        self._write_csv_row(file_name, row)
        if collection == "persons":
            self._write_person_movie_csv(doc)

    def exists_id(self, docId, collection="movies"):
        """
        Check if ID exists
        """
        col = self._db.collection(collection)
        if col is None:
            return False
        search_result = col.filter(lambda x: x["id"] == str.encode(docId))
        if not search_result:
            return False
        return len(search_result) > 0

    def is_movie_rated(self, movie_info, user_id):
        """
        Check if user has rated a movie
        """
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

    def add_user_rate(self, movie_info, user_id):
        """
        Add movie rate to user - create user if not exist
        """
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
                    'movie': {'id': movie_info["id"],
                              'title': movie_info["title"]}}
        if not search_result:
            # user not exist
            user_info = {"id": user_id,
                         "name": name,
                         "ratings": [new_rate]}
            self.write(user_info, collection="users")
            if CSV:
                self._write_user_movie_csv(user_info)
            return
        user = search_result[0]
        user["ratings"].append(new_rate)
        col.update(user["__id"], user)
        self._db.commit()
        if CSV:
            self._write_user_movie_csv(user)
