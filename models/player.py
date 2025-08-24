from tinydb import TinyDB, Query
db = TinyDB('data.json')

class Player:
    def __init__(self, id = None, name = None, surname = None, birthdate = None, score = 0.0):
        self.id = id #National chess ID        
        self.surname = surname
        self.name = name
        self.birthdate = birthdate
        self.score = score

    def add_score(self, points):
        self.score += points
    
    def save_json(self):
        table = db.table("players")
        table.insert({
            "National chess ID": self.id,
            "Surname": self.surname,
            "Name": self.name,
            "Birthdate": self.birthdate,
            "Score": self.score
        })

    def show_players_json(self):
        table = db.table("players")
        players_list = []
        for item in table.all():
            players_list.append(item)
        
        return players_list


    def __str__(self):
        return self.surname, self.name, self.birthdate, self.id, self.score
    