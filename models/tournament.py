from tinydb import TinyDB, Query
db = TinyDB('data.json')
from .player import Player

class Tournament:
    def __init__(self, tournament_name, place, rounds_number = 3, players = []):
        self.name = tournament_name
        self.place = place
        self.rounds_number = rounds_number
        self.players = players

    def add_players_fromID(self, id):

        # Parcourir les joueurs
        table = db.table("players")
        current_player = None
        for player in table.all():
            if player.get("National chess ID") == id:
                current_player = player
                break

        if current_player:
            name      = current_player["Name"]
            surname   = current_player["Surname"]
            birthdate = current_player["Birthdate"]
            score     = current_player["Score"]
            current_player = Player(id, name, surname, birthdate, score)
            self.players.append(current_player)
            return self, current_player
            
        else:
            return None
