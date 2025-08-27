from tinydb import TinyDB, Query
db = TinyDB('data/players.json')

class Player:
    def __init__(self, id, name, surname, birthdate, score = 0.0):
        self.id = id #National chess ID     
        self.surname = surname
        self.name = name
        self.birthdate = birthdate
        self.score = score

    def save_json(self):
        table = db.table("players")
        table.insert({
            "National chess ID": self.id,
            "Surname": self.surname,
            "Name": self.name,
            "Birthdate": self.birthdate,
        })


    def __str__(self):
        return self.surname, self.name, self.birthdate, self.id
    