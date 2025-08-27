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

    def save_json(self):
        tournament_table.upsert({
            "Tournament name": self.name,
            "Start date" : self.start_date,
            "End date": self.end_date,
            "Place": self.place,
            "Rounds number": self.rounds_number,
            "Players": self.players,
        }, (Query()['Tournament name'] == self.name))