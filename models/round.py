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
        

    def generate_round(self, tournament):
        pass

    def create_round_menu(self, tournament_id) :
        """
        create a new round"""
        tournaments = Tournament.get_all_tournaments()
        tournament_details = tournaments[tournament_id]
        rounds_list = tournament_details["rounds_list"]
        players = tournament_details["players"]
        current_round = tournament_details["current_round"]
        self.view.show_play_tournament_menu()
        user_input = self.view.get_input("\nSelect an option : ")
        if user_input == "1" or user_input == "1)" :
            if current_round["state"] == "in_progress" :
                self.view.show_message("Please update the last round before to create a new one")
            else :
                if tournament_details["state"] == "not_started" :
                    Tournament.update_state_tournament(tournament_id, "in_progress")
                Round(tournament_id).update_current_round(current_round["round_number"] + 1, "in_progress_test")
                new_round = self.generate_round(tournament_details)
                self.view.show_message(new_round)
        elif user_input == "2" or user_input == "2)" :
            pass
        elif user_input == "3" or user_input == "3)" :
            pass
        elif user_input == "4" or user_input == "4)" :
            break












