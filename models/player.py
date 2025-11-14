from tinydb import TinyDB, Query
db_players = TinyDB("data/players.json")
players_table = db_players.table("players")

class Player:
    """
    A class representing a chess player, storing details (National Chess ID, name, surname, birthdate).
    It provides methods to save player data to a JSON
    database and retrieve player information.
    """

    def __init__(self, national_chess_id, name, surname, birthdate):
        """
        Initialize a Player instance with the provided details.

        Args:
            national_chess_id : The National Chess ID of the player.
            name : The player's first name.
            surname : The player's surname.
            birthdate : The player's birthdate.
        """
        self.national_chess_id = national_chess_id
        self.name = name   
        self.surname = surname
        self.birthdate = birthdate
        

    def serialize(self):
        """Return a dict"""
        player_serialized = {
            "national_chess_id": self.national_chess_id,
            "surname": self.surname,
            "name": self.name,
            "birthdate": self.birthdate,
        }
        return player_serialized

    @classmethod
    def deserialize(cls, national_chess_id):
        """Return the player object from the national chess id entered"""
        players_list = Player.deserialize_all_players()
        player = next((player for player in players_list if player.national_chess_id == national_chess_id), None)
        return player
    
    @classmethod
    def deserialize_all_players(cls) :
        """ return a list of all players object """
        players = []
        for player in players_table.all():
            national_chess_id = player["national_chess_id"]
            name = player["name"]
            surname = player["surname"]
            birthdate = player["birthdate"]
            player = Player(national_chess_id, name, surname, birthdate)     
            players.append(player)

        return players

    def save_json(self):
        """
        Save the player's details to the players JSON database using TinyDB.
        """
        players_table.insert(self.serialize())