from models import Tournament, Player, Round
from .players_controller import PlayersController
from datetime import datetime


class TournamentsController:
    """
    A controller class for managing tournament.
    It provides methods to create a new tournament in tournaments.json and add new players to a tournament
    """

    def __init__(self, view):
        """
        Initialize a TournamentsController instance.

        Args:
            view: An instance of the View class
        """
        self.view = view
        self.players_controllers = PlayersController(self.view)
        self.round = RoundController(self.view)

    def create(self):
        """
        Collect new tournament details and save it in tournaments.json by using the methods save_json of the model Tournament
        """
        self.view.show_message("\n[bold green]Create tournament[/bold green]\n")
        self.view.show_message("Enter the new tournament details below : ")
        tournament_name = self.view.get_input("Tournament name : ").upper()
        place = self.view.get_input("Place : ")
        start_date = self._get_valid_date("Start date (DD/MM/YYYY) : ")
        number_of_rounds = self._get_valid_number_of_rounds()
        tournament = Tournament(tournament_name, place, start_date, number_of_rounds)
        tournament.save_json()


    def manage_tournaments(self):
        """
        Display the tournament management menu, collect the user selection and delegates tasks to the TournamentsController
        for creating tournaments, adding players, playing tournaments, or go back.
        """

        while True :
            self.view.show_tournaments_menu()
            user_choice = self.view.get_input("\nChoose an option : ")
            if user_choice == "1" or user_choice == "1)":
                self.create()
            elif user_choice == "2" or user_choice == "2)":
                tournament = self._select_tournament()
                self.add_player_tournament(tournament)
            elif user_choice == "3" or user_choice == "3)":
                self.play_tournament()
            elif user_choice == "4" or user_choice == "4)":   
                break

    def add_player_tournament(self, tournament):
        """
        Add players to a tournament in tournaments.json

        Args:
            tournament_name : The name of the tournament to add players to.
                              If None, prompts the user to enter a tournament name.

        Collect the tournament name if not provided and add player to the tournament in tournaments.json.
        If a player doesn't exist, offers the option to create a new player or try again.
        """
            
        while True :  
            self.view.show_add_players_tournament_menu(tournament)
            user_choice = self.view.get_input("\nChoose an option : ")
            if user_choice in ["1","1)"]:
                self._add_single_player_tournament(tournament)
            elif user_choice in ["2","2)"]:
                break

    def _add_single_player_tournament(self, tournament) :
        while True : 
            national_chess_id = self.players_controllers._get_valid_national_chess_id()
            player = Player.deserialize(national_chess_id)
            if player != None:
                tournament.players.append(player)
                tournament.save_json()
                self.view.show_message(f"\n{player.name} {player.surname} ({player.national_chess_id}) was successfully added to the tournament !")
                break
            elif player is None:
                self.view.show_message("\nThis player is not in the database :\n1) Type again \n2) Create a new player \n")
                user_choice = self.view.get_input("Choose an option : ")
                if user_choice in ["1","1)"]:
                    continue
                elif user_choice in ["2","2)"]:
                    player = self.players_controllers.add_player(national_chess_id)
                    tournament.players.append(player)
                    tournament.save_json()
                    self.view.show_message(f"\n{player.name} {player.surname} ({player.national_chess_id}) was successfully added to the tournament !")

                    break

    def play_tournament(self, tournament_id = None):
        

        while tournament_id == None :
            tournament = self._select_tournament()

        while True :
            self.view.show_play_tournament_menu()
            user_choice = self.view.get_input("\nSelect an option : ")
            if user_choice in ["1","1)"] :
                self.round.create_round_menu(tournament)
            elif user_choice in ["2","2)"] :
                self.round.update_results_games(tournament_id)
            elif user_choice in ["3","3)"] :
                pass
            elif user_choice in ["4","4)"] :
                break

    def _select_tournament(self) :
        """Show the list of all tournaments and the user select
        Return the tournament object selected """

        while True:
            tournaments = Tournament.deserialize_all_tournaments()
            self.view.show_tournaments_list(tournaments)
            user_input = self.view.get_input("\nSelect a tournament :")

            if int(user_input) > len(tournaments):
                self.view.show_message("No tournament was find with that ID. Please try again.")
            else:
                tournament_index = int(user_input)-1
                tournament = tournaments[tournament_index]
                return tournament
            
    def _get_valid_number_of_rounds(self) :
        "return a valid number of rounds (int)"
        while True :
            number_of_rounds = self.view.get_input("Number of rounds : ")
            try:
                number_of_rounds = int(number_of_rounds)
                if number_of_rounds > 0:
                    return number_of_rounds
                else:
                    self.view.show_message("Please enter a number greater than 0.")
            except ValueError as e:
                self.view.show_message(f"Invalid input: {e}")

    def _get_valid_date(self, input) :
        "return a valid number of rounds (int)"
        while True :
            date = self.view.get_input(input)
            try:
                datetime.strptime(date, "%d/%m/%Y")
                return date
            except ValueError as e:
                self.view.show_message(f"Invalid input: {e}")


class RoundController :
    
    def __init__(self, view):
        self.view = view

    def create_round_menu(self, tournament) :
        """
        Display the games of the new round
        """
        
        rounds = tournament.rounds
        current_round = tournament.current_round
        actual_round = rounds[current_round-1]

        while True :
            if actual_round.state == "in_progress" :
                self.view.show_message("Please update the current round before to create a new one")
                break
            else :
                new_round = self.generate_round(tournament) 
                #new_rounds should have the "in progres" state
                tournament.rounds.append(new_round)
                tournament.current_round += 1
                tournament.state = "in progress"
                tournament.save_json()
                self.view.show_games_list(new_round)
                break
 
    def update_results_games(self, tournament):
    
        rounds = tournament.rounds
        current_round = tournament.current_round
        actual_round = rounds[current_round-1]
        
        if actual_round.state == "in_progress" :
            for game in actual_round.games_list :
                winner = self.view.update_game_result(game)
                #Tournament.update_score(tournament_id, winner)
                #Tournament.update_element(tournament_id, "current_round", {"round_number": current_round["round_number"] + 1, "state": "in_progress"})
        else :
            self.view.show_message("All rounds are up to date ! Cr")

    def generate_round(self, tournament) :
        pass

    def generate_round_beta(self, tournament_id):
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
            
        tournament_details = Tournament.get_tournament_details(tournament_id)
        players = tournament_details["players"]
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

                if have_played_before(player, opponent, tournament_details["rounds_list"]):
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

        Tournament.update_element(tournament_id, "rounds_list", new_round )
        return new_round
    


    def create_round_menu_beta(self, tournament_id) :
        """
        Display the games of the new round
        """

        tournament_details = Tournament.get_tournament_details(tournament_id)
        current_round = tournament_details["current_round"]

        while True :
            if tournament_details["state"] == "not_started" :
                Tournament.update_element(tournament_id, "state", "in_progress")
            # Output selon l'etat du round :
            if current_round["state"] == "in_progress" :
                self.view.show_message("Please update the current round before to create a new one")
                break
            elif current_round["state"] == None or current_round["state"] == "finished"  :
                new_round = self.generate_round(tournament_id)
                Tournament.update_element(tournament_id, "current_round", {"round_number": current_round["round_number"] + 1, "state": "in_progress"})
                self.view.show_games_list(new_round)
                break


    def update_results_games_beta(self, tournament_id):
        tournament_details = Tournament.get_tournament_details(tournament_id)
        current_round = tournament_details["current_round"]
        if tournament_details["current_round"]["state"] == "in_progress" :
            last_round = Round.get_last_round(tournament_id)
            for game in last_round :
                winner = self.view.update_game_result(game)
                Tournament.update_score(tournament_id, winner)
            Tournament.update_element(tournament_id, "current_round", {"round_number": current_round["round_number"] + 1, "state": "in_progress"})
        else :
            self.view.show_message("No round to update")
     
