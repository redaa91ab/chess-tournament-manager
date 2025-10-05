from config import DATA_PLAYERS_PATH, DATA_TOURNAMENTS_PATH
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

    def __init__(self, tournament_name, place, start_date, end_date, number_of_rounds = 4):
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
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.players = []
        self.rounds_list = []
        self.current_round = 1
        self.manager_comment = None
        self.state = "not_started"


    @classmethod
    def get_all_tournaments(cls) :
        tournaments = {}
        for tournament in tournament_table.all():
                tournaments[tournament.doc_id] = tournament

        return tournaments
            

    def save_json(self):
        """
        Save the tournament's details to the tournaments JSON database.
        """
        tournament_table.upsert({
            "tournament_name": self.tournament_name,
            "start_date" : self.start_date,
            "end_date": self.end_date,
            "place": self.place,
            "number_of_rounds": self.number_of_rounds,
            "players": self.players,
            "current_round" : self.current_round,
            "rounds_list" : self.rounds_list,
            "manager_comment" : self.manager_comment,
            "state": self.state
        }, (Query()['tournament_name'] == self.tournament_name))

    @classmethod
    def get_tournament_details(cls, tournament_name):
        """
        Retrieve details of a tournament by its name from the JSON database.

        Args:
            tournament_name : The name of the tournament to retrieve.

        Returns:
            list or None: A list containing the tournament's details or None.
        """
        TournamentQuery = Query()
        tournament = tournament_table.get(TournamentQuery["Tournament name"] == tournament_name)

        if tournament:
            return {
                "tournament_name": tournament["tournament_name"],
                "start_date": tournament["start_date"],
                "end_date": tournament["end_date"],
                "place": tournament["place"],
                "number_of_rounds": tournament["number_of_rounds"],
                "players": tournament["players"],
                "current_round": tournament["current_round"],
                "rounds_list": tournament["rounds_list"],
                "manager_comment": tournament["manager_comment"],
                "state": tournament["state"]
                }
        else:
            return None

    @classmethod
    def add_player(cls, tournament_id, player):
        """
        Add a player to the specified tournament in the JSON database.

        Args:
            tournament_name : The name of the tournament to add the player to
            player : The National Chess ID of the player to add.

        Updates the tournament's player list in the database.
        """
        tournament = tournament_table.get(doc_id=int(tournament_id))
    
        players = tournament.get("players") or []  # si None -> []
        players.append([player, 0.0])

        tournament_table.update({"players": players}, doc_ids=[int(tournament_id)])

    @classmethod
    def add_round(cls, tournament_name, round):
        """ Update the rounds_list of the tournament by adding the round (list of games) to the list
        """
        TournamentQuery = Query()
        tournaments = tournament_table.search(TournamentQuery["tournament_name"] == tournament_name)

        if tournaments:
            tournament = tournaments[0]
            rounds_list = tournament.get("rounds_list", [])
            rounds_list.append(round)
            tournament_table.update({"rounds_list": rounds_list}, TournamentQuery["tournament_name"] == tournament_name)

    
