from config import DATA_TOURNAMENTS_PATH
from tinydb import TinyDB, Query
from .player import Player
import uuid 
db_tournaments = TinyDB(DATA_TOURNAMENTS_PATH)
tournament_table = db_tournaments.table("tournaments")

class Tournament:
    """
    A class representing a chess tournament, storing details such as name, location, dates,
    rounds, and players. 

    It provides methods to save tournament data to a JSON file and
    retrieve or update tournament information.
    """

    def __init__(self, tournament_name, place, start_date, number_of_rounds = 4, end_date = None, players = [], rounds = [],
                 current_round = 0, previous_opponents = None, manager_comment = None, state = "not_started", tournament_id = None):
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
        self.number_of_rounds = number_of_rounds
        self.end_date = end_date
        self.players = players
        self.rounds = rounds
        self.current_round = current_round
        self.previous_opponents = previous_opponents
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
            "number_of_rounds": self.number_of_rounds,
            "end_date": self.end_date,
            "players": [player.national_chess_id for player in self.players],
            "rounds" : [round.serialize() for round in self.rounds],
            "current_round" : self.current_round,
            "previous_opponents" : self.previous_opponents,
            "manager_comment" : self.manager_comment,
            "state": self.state,
            "tournament_id": self.tournament_id
        }
        return serialized_data
    
    @classmethod
    def deserialize(cls, tournament_id):
        """ Return the tournament object of the tournament_id matching"""
        tournaments_list = Tournament.deserialize_all_tournaments()
        tournament = next((tournament for tournament in tournaments_list if tournament.tournament_id == tournament_id), None)
        return tournament

    def save_json(self):
        """ Save the tournament's details to the tournaments JSON database. """
        
        if self.tournament_id is None :
            self.tournament_id = self.generate_tournament_id()
            tournament_table.insert(self.serialize())
        else :
            tournament_table.update(self.serialize(), (Query()["tournament_id"] == self.tournament_id))

    
    @classmethod
    def deserialize_all_tournaments(cls) :
        """ return a list of all tournament object """
        tournaments = []
        
        for tournament in tournament_table.all():
            tournament_name = tournament["tournament_name"]
            place = tournament["place"]
            start_date = tournament["start_date"]
            number_of_rounds = tournament["number_of_rounds"]
            end_date = tournament["end_date"]
            players = [Player.deserialize(player) for player in tournament["players"]]
            rounds = [Round.deserialize(round) for round in tournament["rounds"]]
            current_round = tournament["current_round"]
            previous_opponents = tournament["previous_opponents"]
            manager_comment = tournament["manager_comment"]
            state = tournament["state"]
            tournament_id = tournament["tournament_id"]


            tournament = Tournament(tournament_name, place, start_date, number_of_rounds, end_date, players,rounds, current_round,
                                            previous_opponents, manager_comment, state, tournament_id)     
            tournaments.append(tournament)

        return tournaments

    @classmethod
    def get_all_tournaments(cls) :
        """ return a dict of all tournament """
        tournaments = {}
        for tournament in tournament_table.all():
                tournaments[tournament.doc_id] = tournament
        return tournaments
  
    @classmethod
    def get_tournament_details(cls, tournament_id):
        """
        Retrieve details of a tournament by its name from the JSON database.

        Args:
            tournament_name : The name of the tournament to retrieve.

        Returns:
            list or None: A list containing the tournament's details or None.
        """
        tournament = tournament_table.get(doc_id=int(tournament_id))

        if tournament:
            return tournament
        else:
            return None
        
    @classmethod
    def update_element(cls, tournament_id, element_to_update, new_element) :
        """
        If the data to update is something to add
        elif it's the whole element to remplace
        """
        if element_to_update == "rounds_list" or element_to_update == "players" :#2 WAYS players = add or change  
        
            tournament = tournament_table.get(doc_id=int(tournament_id))
            data = tournament.get(element_to_update) or []  # if == None return []
            data.append(new_element)
            tournament_table.update({element_to_update: data}, doc_ids=[int(tournament_id)])
        else :
            tournament_table.update({element_to_update: new_element}, doc_ids=[tournament_id])

    @classmethod
    def update_score(cls, tournament_id, winner_nid) :
        """
        If the data to update is something to add
        elif it's the whole element to remplace
        """
        tournament = tournament_table.get(doc_id=int(tournament_id))
        players = tournament.get("players")
        print(players)
        new_players = []
        for player in players :
            print(player)
            if player[0] == winner_nid :
                player_updated = [player[0], player[1]+1]
                new_players.append(player_updated)
            else :
                new_players.append(player)
        
        tournament_table.update({"players": new_players}, doc_ids=[tournament_id])
        

class Round :
    def __init__(self, name, games_list, state): 
        self.name = name #ROUND 1, etc...
        self.games_list = games_list #liste objets games
        self.state = state

    def serialize(self):
        serialized_data = {
            "name" : self.name,
            "games_list" : [game.serialize() for game in self.games_list], #serialiser deserialiser#
            "state" : self.state
            } 
        
        return serialized_data
               
    @classmethod
    def deserialize(cls, round_serialized):
        name = round_serialized["name"]
        games_list = round_serialized["games_list"] #serialiser deserialiser#
        state = round_serialized["state"]

        round_deserialized = Round(name, games_list, state)
        return round_deserialized


    @classmethod
    def get_last_round(cls, tournament_id):
        tournament_details = Tournament.get_tournament_details(tournament_id)
        rounds_list = tournament_details["rounds_list"]
        return rounds_list[-1]
    

class Game :
    def __init__(self, player1, score_player1, player2, score_player2):
        self.player1 = player1
        self.score_player1 = score_player1
        self.player2 = player2
        self.score_player2 = score_player2

    def serialize(self):
        serialized_data = {
            ([self.player1, self.score_player1], [self.player2, self.score_player2])
        }
        return serialized_data
    
    @classmethod
    def deserialize(cls, game) :
        player1 = game.player1
        score_player1 = game.score_player1
        player2 = game.player2
        score_player2 = game.score_player2

        game_deserialized = Round(player1, score_player1, player2, score_player2)
        return game_deserialized

    #serialiser deserialiser#




    
    
    

    
