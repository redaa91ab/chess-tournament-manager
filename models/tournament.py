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

    def __init__(self, tournament_name, place, start_date, end_date, number_of_rounds = 4, players = [], rounds_list = []):
        """
        Initialize a Tournament instance with the provided details.

        Args:
            tournament_name : The name of the tournament.
            place : The location of the tournament.
            start_date : The start date of the tournament.
            end_date : The end date of the tournament.
            number_of_rounds : The number of rounds in the tournament. Defaults to 4.
            players : A list of player National Chess IDs. Defaults to an empty list.

        """
        self.tournament_name = tournament_name.upper()
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.players = players
        self.actual_round = 1
        self.rounds_list = rounds_list
        self.manager_comment = None


    def save_json(self):
        """
        Save the tournament's details to the tournaments JSON database.
        """
        tournament_table.upsert({
            "Tournament name": self.tournament_name,
            "Start date" : self.start_date,
            "End date": self.end_date,
            "Place": self.place,
            "Number of rounds": self.number_of_rounds,
            "Players": self.players,
            "Actual round" : self.actual_round,
            "Rounds list" : self.rounds_list,
            "Manager comment" : self.manager_comment
        }, (Query()['Tournament name'] == self.tournament_name))

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
                "Tournament name": tournament["Tournament name"],
                "Start date": tournament["Start date"],
                "End date": tournament["End date"],
                "Place": tournament["Place"],
                "Number of rounds": tournament["Number of rounds"],
                "Players": tournament["Players"],
                "Actual round": tournament["Actual round"],
                "Rounds list": tournament["Rounds list"],
                "Manager comment": tournament["Manager comment"]
                }
        else:
            return None

    @classmethod
    def add_player(cls, tournament_name, player):
        """
        Add a player to the specified tournament in the JSON database.

        Args:
            tournament_name : The name of the tournament to add the player to.
            player : The National Chess ID of the player to add.

        Updates the tournament's player list in the database.
        """
        TournamentQuery = Query()
        tournaments = tournament_table.search(TournamentQuery["Tournament name"] == tournament_name)

        if tournaments:
            tournament = tournaments[0]
            players = tournament.get("Players", [])
            players.append([player, 0.0])
            tournament_table.update({"Players": players}, TournamentQuery["Tournament name"] == tournament_name)

    
    @classmethod
    def add_round(cls, tournament_name, round):
        """ Update the rounds_list of the tournament by adding the round (list of games) to the list
        """
        TournamentQuery = Query()
        tournaments = tournament_table.search(TournamentQuery["Tournament name"] == tournament_name)

        if tournaments:
            tournament = tournaments[0]
            rounds_list = tournament.get("Rounds list", [])
            rounds_list.append([round])
            tournament_table.update({"Rounds list": round}, TournamentQuery["Tournament name"] == tournament_name)

    

