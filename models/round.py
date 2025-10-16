from config import DATA_PLAYERS_PATH, DATA_TOURNAMENTS_PATH
from tinydb import TinyDB, Query
db_tournaments = TinyDB(DATA_TOURNAMENTS_PATH)
db_players = TinyDB(DATA_PLAYERS_PATH)
tournament_table = db_tournaments.table("tournaments")


class Round :
    def __init__(self, tournament_id):
        self.tournament_id = tournament_id        

    def update_current_round(self,new_round_number, new_state):
        self.state = new_state
        tournament_table.update({"current_round": {"round_number" : new_round_number, "state" : new_state}}, doc_ids=[self.tournament_id])

    def generate_round(self, tournament_id):
        pass

    












