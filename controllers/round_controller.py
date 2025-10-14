from models import Round, Tournament

class RoundController :
    
    def __init__(self, view, parent = None):
        self.view = view
        self.parent = parent

    def create_round_menu(self, tournament_id) :
        """
        Display the games of the new round
        """
        tournaments = Tournament.get_all_tournaments()
        tournament_details = tournaments[tournament_id]
        current_round = tournament_details["current_round"]
        #self.view.show_play_tournament_menu()
        #user_input = self.view.get_input("\nSelect an option : ")


        while True :
            if current_round["state"] == "in_progress" :
                self.view.show_message("Please update the last round before to create a new one")
            else :
                if tournament_details["state"] == "not_started" :
                    Tournament.update_state_tournament(tournament_id, "in_progress")
                Round(tournament_id).update_current_round(current_round["round_number"] + 1, "in_progress_test")
                new_round = self.generate_round(tournament_details)
                self.view.show_message(new_round)

        
    def generate_round(self, tournament):
        """
        return a list new round for the tournament, based on actual players, score, and past rounds.

        Args :
            tournament : The tournament where to generate
        
        """
        
        def have_played_before(p1, p2, past_rounds):
            """
            return True if the two players have played in the past rounds on this tournament
            else return False 

            Args : 
                p1 and p2 : The two players
                past_rounds : The past rounds of the tournament
        
            """
            p1 = p1[0]
            p2 = p2[0]
            for rnd in past_rounds:
                for match in rnd:
                    if (p1 == match[0][0] and p2 == match[1][0]) or (p1 == match[1][0] and p2 == match[0][0]):
                        return True
            return False
            
        players = tournament["players"]
        players.sort(key=lambda x: x[1])
        
        new_round = [] # liste des matchs du round
        used_players = []

        for player in players:
            if player in used_players:
                continue  # ce joueur est déjà apparié

            # chercher un adversaire
            for opponent in players:
                if opponent in used_players or opponent == player:
                    continue

                if have_played_before(player, opponent, tournament["rounds_list"]):
                    continue
                
                else :
                    new_round.append((player, opponent))
                    used_players.extend([player, opponent])
                    break # on passe au joueur suivant

            if player not in used_players :
                for opponent in players:
                    if opponent not in used_players and opponent != player:
                        new_round.append((player, opponent))
                        used_players.extend([player, opponent])
                        break

        Tournament.add_round(tournament["tournament_name"], new_round)
        return new_round
