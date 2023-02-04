import json
#from movie import Movie

PATH = "./data"

class Celeb:

    def __init__(self, name: str, profession: list, works: list):
        self.name = name
        self.profession = profession
        self.works = works

    
    def get_json(self) -> dict:
        return json.dumps(self, default=lambda o: o.__dict__)

    def store(self):
        filename = self.name.split(" ")
        filename = "_".join(filename)
        filename = f"{filename.lower()}.json"
        path = f"{PATH}/{filename}"
        with open(path, 'w') as f:
            json.dump(self.get_json(), f, indent = 6)

