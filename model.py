from tinydb import TinyDB, Query
db = TinyDB('data.json')


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
            print(f"{surname} {name} ({id}) was successfully added !")
            self.players.append(Player(id, name, surname, birthdate, score))
            return self
        else:
            print("We need more information to add your player ")
            return None



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
    
    def __str__(self):
        return self.surname, self.name, self.birthdate, self.id, self.score
    

class Json :
    def __init__(self):
        self.db = db

    def show_players(self) :
        table = self.db.table("players")
        print("")
        for item in table.all():
            print(item)




        




