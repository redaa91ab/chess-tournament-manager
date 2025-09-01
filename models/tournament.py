from tinydb import TinyDB, Query
db_players = TinyDB('data/players.json')
db_tournaments = TinyDB('data/tournaments.json')
tournament_table = db_tournaments.table("tournaments")


class Tournament:
    """
    A class representing a chess tournament, storing details such as name, location, dates,
    rounds, and players. 

    It provides methods to save tournament data to a JSON file and
    retrieve or update tournament information.
    """

    def __init__(self, tournament_name, place, start_date, end_date, rounds_number = 3, players = []):
        """
        Initialize a Tournament instance with the provided details.

        Args:
            tournament_name : The name of the tournament.
            place : The location of the tournament.
            start_date : The start date of the tournament.
            end_date : The end date of the tournament.
            rounds_number : The number of rounds in the tournament. Defaults to 3.
            players : A list of player IDs. Defaults to an empty list.

        """

        self.name = tournament_name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.rounds_number = rounds_number
        self.players = players
        self.actual_round = 1
        self.rounds_list = []
        self.manager_comment = None

    def save_json(self):
        """
        Save the tournament's details to the tournaments JSON database.
        """
        tournament_table.upsert({
            "Tournament name": self.name,
            "Start date" : self.start_date,
            "End date": self.end_date,
            "Place": self.place,
            "Rounds number": self.rounds_number,
            "Players": self.players,
            "Actual round" : self.actual_round,
            "Rounds list" : self.rounds_list,
            "Manager comment" : self.manager_comment
        }, (Query()['Tournament name'] == self.name))


    @classmethod
    def tournament_details(cls, tournament_name):
        """
        Retrieve details of a tournament by its name from the JSON database.

        Args:
            tournament_name : The name of the tournament to retrieve.

        Returns:
            list or None: A list containing the tournament's details or None.
        """
        TournamentQuery = Query()
        tournaments = tournament_table.search(TournamentQuery["Tournament name"] == tournament_name)


        if tournaments:
            tournament = tournaments[0]
            tournament_name = tournament.get("Tournament name", [])
            start_date = tournament.get("Start date", [])
            end_date = tournament.get("End date", [])
            place = tournament.get("Place", [])
            rounds_number = tournament.get("Rounds number", [])
            players = tournament.get("Players", [])
            actual_round = tournament.get("Actual round", [])
            rounds_list = tournament.get("Rounds list", [])
            manager_comment = tournament.get("Manager comment", [])

            tournament = [tournament_name, start_date, end_date, place, rounds_number, players, actual_round, rounds_list, manager_comment]

            return tournament
        else :
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
            players.append(player)
            tournament_table.update({"Players": players}, TournamentQuery["Tournament name"] == tournament_name)


    

