from tinydb import TinyDB, Query
db_players = TinyDB('data/players.json')

class Player:
    def __init__(self, id, name, surname, birthdate, score = 0.0):
        self.id = id #National chess ID     
        self.surname = surname
        self.name = name
        self.birthdate = birthdate
        self.score = score

    def save_json(self):
        table = db_players.table("players")
        table.insert({
            "National chess ID": self.id,
            "Surname": self.surname,
            "Name": self.name,
            "Birthdate": self.birthdate,
        })

    @classmethod
    def players_list(cls):
        table = db_players.table("players")
        players_list = []
        for item in table.all():
            players_list.append(item)
        
        return players_list
    
    @classmethod
    def return_player_details(cls, id):
        # Parcourir les joueurs
        table = db_players.table("players")
        current_player = None
        for player in table.all():
            if player.get("National chess ID") == id:
                current_player = player
                break

        if current_player:
            name      = current_player["Name"]
            surname   = current_player["Surname"]
            birthdate = current_player["Birthdate"]
            
            current_player = [id, name, surname, birthdate]
            return current_player
            
        else:
            return None

    def __str__(self):
        return self.surname, self.name, self.birthdate, self.id
    