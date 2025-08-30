from tinydb import TinyDB, Query
db_players = TinyDB('data/players.json')
db_tournaments = TinyDB('data/tournaments.json')
tournament_table = db_tournaments.table("tournaments")


class Tournament:
    def __init__(self, tournament_name, place, start_date, end_date, rounds_number = 3, players = []):
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





    def return_details(self, tournament_name):
        TournamentQuery = Query()
        tournaments = tournament_table.search(TournamentQuery["Tournament name"] == tournament_name)

        
        if tournaments:
            tournament = tournaments[0]
            players = tournament.get("Players", [])
            tournament_table.update({"Players": players}, TournamentQuery["Tournament name"] == tournament_name)
        else :
            return None




    @classmethod
    def add_player(cls, tournament_name, player):
        TournamentQuery = Query()
        tournaments = tournament_table.search(TournamentQuery["Tournament name"] == tournament_name)

        if tournaments:
            tournament = tournaments[0]
            players = tournament.get("Players", [])
            players.append(player)
            tournament_table.update({"Players": players}, TournamentQuery["Tournament name"] == tournament_name)


    

