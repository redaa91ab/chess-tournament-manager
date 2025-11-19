from tinydb import TinyDB, Query
from .player import Player
import uuid 
db_tournaments = TinyDB("data/tournaments.json")
tournament_table = db_tournaments.table("tournaments")

class Tournament:
    """
    A class representing a chess tournament

    It provides methods to save tournament data to JSON and
    retrieve or update tournament information.
    """

    def __init__(self, tournament_id, tournament_name, place, start_date, end_date = None, number_of_rounds = 4,current_round = 0, players = [], rounds = [],
                manager_comment = None, state = "not_started"):
        """
        Initialize a Tournament instance with the provided details.

        Args:
            tournament_id : Unique id for the tournament
            tournament_name : The name of the tournament.
            place : The location of the tournament.
            start_date : The start date of the tournament.
            end_date : The end date of the tournament.
            number_of_rounds : The number of rounds in the tournament. Defaults to 4.
            current_round : The number of the round that is actually playing
            players : List of PlayerTournament objects
            rounds : List of round objects
            manager_comment : Comment of the manager
            state : state of the tournament
        """
        self.tournament_id = tournament_id
        self.tournament_name = tournament_name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.players = players
        self.rounds = rounds
        self.manager_comment = manager_comment
        self.state = state

    @classmethod
    def generate_tournament_id(cls):
        """ return a tournament_id"""
        return str(uuid.uuid4())
    
    def serialize(self):
        """ return a dict of the tournament object """
        serialized_data = {
            "tournament_id": self.tournament_id,
            "tournament_name": self.tournament_name,
            "place": self.place,
            "start_date" : self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round" : self.current_round,
            "players": [player.serialize() for player in self.players],
            "rounds" : [round.serialize() for round in self.rounds],
            "manager_comment" : self.manager_comment,
            "state": self.state
        }
        return serialized_data

    def save_json(self):
        """ Save the tournament's details to the tournaments JSON database. """
        
        tournament_table.upsert(self.serialize(), (Query()["tournament_id"] == self.tournament_id))


    @classmethod
    def deserialize(cls, tournament_serialized):
        """ return the tournament object """
        tournament_id = tournament_serialized["tournament_id"]
        tournament_name = tournament_serialized["tournament_name"]
        place = tournament_serialized["place"]
        start_date = tournament_serialized["start_date"]
        end_date = tournament_serialized["end_date"]
        number_of_rounds = tournament_serialized["number_of_rounds"]
        current_round = tournament_serialized["current_round"]
        players = [PlayerTournament.deserialize(player) for player in tournament_serialized["players"]]
        rounds = [Round.deserialize(round, players) for round in tournament_serialized["rounds"]]
        manager_comment = tournament_serialized["manager_comment"]
        state = tournament_serialized["state"]

        tournament = Tournament(tournament_id, tournament_name, place, start_date, end_date, number_of_rounds, current_round, players, rounds,
                                manager_comment, state)
        
        return tournament

    
    @classmethod
    def deserialize_all_tournaments(cls) :
        """ return a list of all tournaments object """

        tournaments = [Tournament.deserialize(tournament) for tournament in tournament_table.all()]

        return tournaments
    
    def get_players_sorted(self):
        """ return a list of the players of the tournament sorted from the highest score to the lowest"""
        players_list = self.players
        players_list_sorted = sorted(players_list, key=lambda player: player.total_score)
        return players_list_sorted
    

    def get_previous_opponents(self, player):
        """ return a list of the previous opponents that the player played against in the tournament """
        previous_opponents = []

        for round in self.rounds :
            previous_opponents_round = round.get_previous_opponents_round(player)
            previous_opponents.append(previous_opponents_round)

        return previous_opponents
    

class Round :
    """
    A class representing a round in the chess tournament

    It provides methods to serialize and deseralize the round, and to get the previous oppponent of a player in the round
    """
    def __init__(self, name, games_list, state, start_date = None, end_date = None): 
        """
        Initialize a round with the provided details.

        Args:
            name : The name of the round (ROUND 1, ROUND 2, etc..).
            games_list : List of game objects
            state : in_progress or finished
            start_date : The start date of the round
            end_date : The end date of the round
        """
        self.name = name
        self.games_list = games_list
        self.state = state
        self.start_date = start_date
        self.end_date = end_date

    def serialize(self):
        """ return a dict of the round object """
        serialized_data = {
            "name" : self.name,
            "games_list" : [game.serialize() for game in self.games_list], 
            "state" : self.state,
            "start_date" : self.start_date,
            "end_date" : self.end_date
            } 
        
        return serialized_data
               
    @classmethod
    def deserialize(cls, round_serialized, players):
        """ return an object of the serialized round """
        name = round_serialized["name"]
        games_list = [Game.deserialize(game, players) for game in round_serialized["games_list"]]
        state = round_serialized["state"]
        start_date = round_serialized["start_date"]
        end_date = round_serialized["end_date"]

        round_deserialized = Round(name, games_list, state, start_date, end_date)
        return round_deserialized
    

    def get_previous_opponents_round(self, player):
        """ return a list of the previous opponents that the player played against in the round"""

        previous_opponents = []
        for game in self.games_list :
                if game.player1 == player :
                    previous_opponents.append(game.player2)
                elif game.player2 == player :
                    previous_opponents.append(game.player1)
        return previous_opponents
    

class Game :
    """
    A class representing a game in the chess tournament

    It provides methods to serialize and deseralize the game
    """
    def __init__(self, player1_tournament, score_player1_tournament, player2_tournament, score_player2_tournament):
        """
        Initialize a game with the provided details.

        Args:
            player1 : first PlayerTournament object 
            player2 : second PlayerTournament object
        """
        self.player1_tournament = player1_tournament
        self.score_player1_tournament = score_player1_tournament
        self.score_player2_tournament = score_player2_tournament
        self.player2_tournament = player2_tournament

   
    def serialize(self):
        """ return a dict of the game object """
        serialized_data = (
            [self.player1_tournament.player.national_chess_id, self.score_player1_tournament],
            [self.player2_tournament.player.national_chess_id, self.score_player2_tournament]
            )
        return serialized_data
    
    @classmethod
    def deserialize(cls, game_serialized, players) :
        "return a game object"
        player1_national_chess_id = game_serialized[0][0]
        
        player1 = PlayerTournament.deserialize(player1_national_chess_id, players)
        score_player1 = game_serialized[0][1]

        player2_national_chess_id = game_serialized[1][0]
        player2 = Player.deserialize(player2_national_chess_id)
        score_player2 = game_serialized[1][1]

        game_deserialized = Game(player1, score_player1, player2, score_player2)

        return game_deserialized


class PlayerTournament(Player) :
    """
    A class representing a player in the chess tournament

    It provides methods to serialize and deseralize the player
    """
    def __init__(self, national_chess_id, name, surname, birthdate, total_points) :
        """
        Initialize a player with the provided details.

        Args:
            player : Player object 
            total_score : total score of the player in the tournament
        """
        super().__init__(national_chess_id, name, surname, birthdate)
        self.total_points = total_points

    def serialize(self):
        """ return a dict of the PlayerTournament object"""
        serialized_data = [
            self.player.national_chess_id,
            self.total_points
            ]
        return serialized_data

    @classmethod
    def deserialize(cls, player_tournament_serialized) :
        """ return a PlayerTournament object """
        
        national_chess_id = player_tournament_serialized[0]
        player = Player.deserialize(national_chess_id)
        total_points = player_tournament_serialized[1]

        player_tournament_deserialized = PlayerTournament(player, total_points)
        
        return player_tournament_deserialized
    
    @classmethod
    def deserialize_by_nid(cls, national_chess_id, players: list):
        player_tournament_deserialized = next((player for player in players if player.national_chess_id == national_chess_id), None)

        return player_tournament_deserialized
    

"""
class PlayerGame :

    def __init__(self, player_tournament, score) :

        self.player = player_tournament.player
        self.player_tournament = player_tournament
        self.score = score


    def serialize(self):
        serialized_data = [
            self.player.national_chess_id,
            self.total_score
        ]
        return serialized_data
    
    @classmethod
    def deserialize(cls, player_game_serialized, players) :

        for tournament in tournament_table.all() :
            if tourn

        #step1 : Pgs = NID & score to total points
        #Pt = player(des_nid) + total points
        #
        #step : PlayerGame(player_tournament, score)
        national_chess_id = player_game_serialized[0]
        player_deserialized = Player.deserialize(national_chess_id)
"""







    
    
    

    
