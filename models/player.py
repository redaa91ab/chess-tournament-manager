from config import DATA_PLAYERS_PATH
from tinydb import TinyDB, Query
db_players = TinyDB(DATA_PLAYERS_PATH)

class Player:
    """
    A class representing a chess player, storing details (National Chess ID, name, surname, birthdate, score).
    It provides methods to save player data to a JSON
    database and retrieve player information.
    """

    def __init__(self, national_chess_id, name, surname, birthdate, score = 0.0):
        """
        Initialize a Player instance with the provided details.

        Args:
            national_chess_id : The National Chess ID of the player.
            name : The player's first name.
            surname : The player's surname.
            birthdate : The player's birthdate.
            score : The player's score in a tournament.
        """
        self.national_chess_id = national_chess_id
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
            "National chess ID": self.national_chess_id,
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
    def get_player_details(cls, national_chess_id):
        """
        Return details of a player by their National Chess ID.

        Args:
            national_chess_id : The National Chess ID of the player to retrieve.

        Returns:
            list or None: A list containing the player's details or None.
        """
        table = db_players.table("players")
        current_player = None
        for player in table.all():
            if player.get("National chess ID") == national_chess_id:
                current_player = player
                break

        if current_player:
            name      = current_player["Name"]
            surname   = current_player["Surname"]
            birthdate = current_player["Birthdate"]
            current_player = [national_chess_id, name, surname, birthdate]
            return current_player
        else:
            return None

    def __str__(self):
        return self.surname, self.name, self.birthdate, self.national_chess_id
    