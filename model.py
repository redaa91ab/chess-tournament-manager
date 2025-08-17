from tinydb import TinyDB, Query
db = TinyDB('data.json')

class Player:
    def __init__(self, surname, name, birthdate, id, score = 0.0):
        self.surname = surname
        self.name = name
        self.birthdate = birthdate
        self.id = id
        self.score = score   

    def add_score(self, points):
        self.score += points
    
    def save_json(self):
        table = db.table("players")
        table.insert({
            "Surname": self.surname,
            "Name": self.name,
            "Birthdate": self.birthdate,
            "National chess ID": self.id,
            "Score": self.score
        })
    
    def __str__(self):
        return self.surname, self.name, self.birthdate, self.id, self.score



