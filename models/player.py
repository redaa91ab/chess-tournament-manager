from config import Data_Players_JSON
from tinydb import TinyDB, Query
db_players = TinyDB(Data_Players_JSON)

class Player:
    """
    A class representing a chess player, storing details (National Chess ID, name, surname, birthdate, score).
    It provides methods to save player data to a JSON
    database and retrieve player information.
    """

    def __init__(self, id, name, surname, birthdate, score = 0.0):
        """
        Initialize a Player instance with the provided details.

        Args:
            id : The National Chess ID of the player.
            name : The player's first name.
            surname : The player's surname.
            birthdate : The player's birthdate.
            score : The player's score in a tournament.
        """
        self.id = id #National chess ID  
        self.name = name   
        self.surname = surname
        self.birthdate = birthdate
        self.score = score

    def save_json(self):
        """
        Save the player's details to the players JSON database using TinyDB.
        """
        table = db_players.table("players")
        table.insert({
            "National chess ID": self.id,
            "Surname": self.surname,
            "Name": self.name,
            "Birthdate": self.birthdate,
        })

    @classmethod
    def get_all_players(cls):
        """
        Return a list of all players.

        Returns:
            list: A list of dictionaries containing the details of each player.
        """
        table = db_players.table("players")
        players_list = []
        for item in table.all():
            players_list.append(item)

        return players_list
    
    @classmethod
    def get_player_details(cls, id):
        """
        Return details of a player by their National Chess ID.

        Args:
            id : The National Chess ID of the player to retrieve.

        Returns:
            list or None: A list containing the player's details or None.
        """
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
    