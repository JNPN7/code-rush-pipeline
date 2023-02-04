import json


class Movie:
    
    def __init__(self, name: str, typ: str, year: str, rating: str, director: str, genre: list):
        self.name = name
        self.type = typ
        self.year = year
        self.rating = rating
        self.director = director
        self.genre = genre


    def get_json(self) -> dict:
        return json.dumps(self.__dict__)


