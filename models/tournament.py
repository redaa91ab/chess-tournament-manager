from config import DATA_TOURNAMENTS_PATH
from tinydb import TinyDB, Query
db_tournaments = TinyDB(DATA_TOURNAMENTS_PATH)
tournament_table = db_tournaments.table("tournaments")

class Tournament:
    """
    A class representing a chess tournament, storing details such as name, location, dates,
    rounds, and players. 

    It provides methods to save tournament data to a JSON file and
    retrieve or update tournament information.
    """

    def __init__(self, tournament_name, place, start_date, number_of_rounds = 4):
        """
        Initialize a Tournament instance with the provided details.

        Args:
            tournament_name : The name of the tournament.
            place : The location of the tournament.
            start_date : The start date of the tournament.
            end_date : The end date of the tournament.
            number_of_rounds : The number of rounds in the tournament. Defaults to 4.
        """
        self.tournament_name = tournament_name.upper()
        self.place = place
        self.start_date = start_date
        self.end_date = None
        self.number_of_rounds = number_of_rounds
        self.players = []
        self.rounds_list = []
        self.current_round = {"round_number" : 0, "state" : None}
        self.previous_opponents = None
        self.manager_comment = None
        self.state = "not_started"

    def serialize(self):
        """
        Serialize the python object of the tournament model to a dict
        """
        serialized_data = {
            "tournament_name": self.tournament_name,
            "place": self.place,
            "start_date" : self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "players": self.players,
            "rounds_list" : self.rounds_list,
            "current_round" : self.current_round,
            "previous_opponents" : self.previous_opponents,
            "manager_comment" : self.manager_comment,
            "state": self.state
        }
        return serialized_data


    def save_json(self):
        """
        Save the tournament's details to the tournaments JSON database.
        """
        tournament_table.upsert(self.serialize(), (Query()['tournament_name'] == self.tournament_name))


    @classmethod
    def get_all_tournaments(cls) :
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
    def __init__(self): 
        pass

    @classmethod
    def get_last_round(self, tournament_id):
        tournament_details = Tournament.get_tournament_details(tournament_id)
        rounds_list = tournament_details["rounds_list"]
        return rounds_list[-1]
    
