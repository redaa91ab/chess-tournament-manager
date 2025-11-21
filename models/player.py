from tinydb import TinyDB

db_players = TinyDB("data/players.json")
players_table = db_players.table("players")

class Player:
    """
    A class representing a chess player and storing details.
    It provides methods to save player to JSON, serialize, deserialize and retrieve player(s) details.
    """

    def __init__(self, national_chess_id, name, surname, birthdate):
        """
        Initialize a Player instance with the all the details.

        Args:
            national_chess_id : The National Chess ID of the player.
            name : The first name.
            surname : The surname.
            birthdate : The birthdate.
        """
        self.national_chess_id = national_chess_id
        self.name = name   
        self.surname = surname
        self.birthdate = birthdate        

    def serialize(self):
        """Return a dict"""
        player_serialized = {
            "national_chess_id": self.national_chess_id,
            "name": self.name,
            "surname": self.surname,
            "birthdate": self.birthdate,
        }
        return player_serialized

    @classmethod
    def deserialize(cls, national_chess_id):
        """Retrieve player's details with nid
        Return the player object"""
        for player in players_table.all():
            if player["national_chess_id"] == national_chess_id :
                national_chess_id = player["national_chess_id"]
                name = player["name"]
                surname = player["surname"]
                birthdate = player["birthdate"]
                player = Player(national_chess_id, name, surname, birthdate)
                return player
    
        return None
    
    @classmethod
    def deserialize_all_players(cls) :
        """ return a list of all players object """

        players = [Player.deserialize(player_serialized["national_chess_id"]) for player_serialized in players_table.all()]

        return players

    def save_json(self):
        """
        Save the player's details to the players JSON database using TinyDB.
        """
        players_table.insert(self.serialize())