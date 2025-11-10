from config import DATA_TOURNAMENTS_PATH
from tinydb import TinyDB, Query
from .player import Player
import uuid 
db_tournaments = TinyDB("data/tournaments.json")
tournament_table = db_tournaments.table("tournaments")
TinyDB("data/tournaments.json").table("tournaments")

class Tournament:
    """
    A class representing a chess tournament, storing details such as name, location, dates,
    rounds, and players. 

    It provides methods to save tournament data to a JSON file and
    retrieve or update tournament information.
    """

    def __init__(self, tournament_name, place, start_date, end_date = None, number_of_rounds = 4,current_round = 0, players = [], rounds = [],
                manager_comment = None, state = "not_started", tournament_id = None):
        """
        Initialize a Tournament instance with the provided details.

        Args:
            tournament_name : The name of the tournament.
            place : The location of the tournament.
            start_date : The start date of the tournament.
            end_date : The end date of the tournament.
            number_of_rounds : The number of rounds in the tournament. Defaults to 4.
        """
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
        self.tournament_id = tournament_id

    def generate_tournament_id(self):
        return str(uuid.uuid4())
    
    def serialize(self):
        """ Serialize the python object of the tournament model and return a dict"""
        serialized_data = {
            "tournament_name": self.tournament_name,
            "place": self.place,
            "start_date" : self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round" : self.current_round,
            "players": [player.serialize() for player in self.players],
            "rounds" : [round.serialize() for round in self.rounds],
            "manager_comment" : self.manager_comment,
            "state": self.state,
            "tournament_id": self.tournament_id
        }
        return serialized_data

    def save_json(self):
        """ Save the tournament's details to the tournaments JSON database. """
        
        if self.tournament_id is None :
            self.tournament_id = self.generate_tournament_id()
        
        tournament_table.upsert(self.serialize(), (Query()["tournament_id"] == self.tournament_id))

    
    @classmethod
    def deserialize_all_tournaments(cls) :
        """ return a list of all tournament object """
        tournaments = []
        
        for tournament in tournament_table.all():
            tournament_name = tournament["tournament_name"]
            place = tournament["place"]
            start_date = tournament["start_date"]
            end_date = tournament["end_date"]
            number_of_rounds = tournament["number_of_rounds"]
            current_round = tournament["current_round"]
            players = [PlayerTournament.deserialize(player) for player in tournament["players"]]
            rounds = [Round.deserialize(round) for round in tournament["rounds"]]
            manager_comment = tournament["manager_comment"]
            state = tournament["state"]
            tournament_id = tournament["tournament_id"]


            tournament = Tournament(tournament_name, place, start_date, end_date, number_of_rounds, current_round, players, rounds,
                                    manager_comment, state, tournament_id)
            tournaments.append(tournament)

        return tournaments
    
    def get_players_sorted(self):
        players_list = self.players
        players_list_sorted = sorted(players_list, key=lambda player: player.score)
        return players_list_sorted
    

    def get_previous_opponents(self, player):
        previous_opponents = []

        for round in self.rounds :
            previous_opponents_round = round.get_previous_opponents_round(player)
            previous_opponents.append(previous_opponents_round)

        return previous_opponents
    

class Round :
    def __init__(self, name, games_list, state, start_date = None, end_date = None): 
        self.name = name
        self.games_list = games_list
        self.state = state
        self.start_date = start_date
        self.end_date = end_date

    def serialize(self):
        serialized_data = {
            "name" : self.name,
            "games_list" : [game.serialize() for game in self.games_list], 
            "state" : self.state,
            "start_date" : self.start_date,
            "end_date" : self.end_date
            } 
        
        return serialized_data
               
    @classmethod
    def deserialize(cls, round_serialized):
        name = round_serialized["name"]
        games_list = [Game.deserialize(game) for game in round_serialized["games_list"]]
        state = round_serialized["state"]
        start_date = round_serialized["start_date"]
        end_date = round_serialized["end_date"]

        round_deserialized = Round(name, games_list, state, start_date, end_date)
        return round_deserialized
    

    def get_previous_opponents_round(self, player):

        previous_opponents = []
        for game in self.games_list :
                if game.player1 == player :
                    previous_opponents.append(game.player2)
                elif game.player2 == player :
                    previous_opponents.append(game.player1)
        return previous_opponents
    

class Game :
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
   
    def serialize(self):
        serialized_data = (
            self.player1.serialize(),
            self.player2.serialize()
            )
        return serialized_data
    
    @classmethod
    def deserialize(cls, game_serialized) :
        player1_serialized = game_serialized[0]
        player1_deserialized = PlayerTournament.deserialize(player1_serialized)
        player2_serialized = game_serialized[1]
        player2_deserialized = PlayerTournament.deserialize(player2_serialized)

        game_deserialized = Game(player1_deserialized, player2_deserialized)
        return game_deserialized


class PlayerTournament :
    def __init__(self, player, score) :
        self.player = player
        self.score = score

    def serialize(self):
        serialized_data = [
            self.player.national_chess_id,
            self.score
            ]
        return serialized_data

    @classmethod
    def deserialize(cls, player_serialized) :
        
        national_chess_id = player_serialized[0]
        player = Player.deserialize(national_chess_id)
        score = player_serialized[1]

        player_deserialized = PlayerTournament(player, score)
        
        return player_deserialized






    
    
    

    
