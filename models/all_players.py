from tinydb import TinyDB, Query
db_players = TinyDB('data/players.json')

class AllPlayers:
    def players_list(self):
        table = db_players.table("players")
        players_list = []
        for item in table.all():
            players_list.append(item)
        
        return players_list
    
    def return_player_details(self, id):
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