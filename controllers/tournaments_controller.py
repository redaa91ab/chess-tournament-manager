from models import Tournament, Player, Round, Game, PlayerTournament
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
                if tournament :
                    self.add_player_tournament(tournament)
            elif user_choice == "3" or user_choice == "3)":
                tournament = self._select_tournament()
                if tournament :
                    self.play_tournament(tournament)
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
                tournament.players.append(PlayerTournament(player, 0.0))
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
                    tournament.players.append(PlayerTournament(player, 0.0))
                    tournament.save_json()
                    self.view.show_message(f"\n{player.name} {player.surname} ({player.national_chess_id}) was successfully added to the tournament !")

                    break

    def play_tournament(self, tournament):

        while True :
            self.view.show_play_tournament_menu()
            user_choice = self.view.get_input("\nSelect an option : ")
            if user_choice in ["1","1)"] :
                self.round.create_round_menu(tournament)
            elif user_choice in ["2","2)"] :
                self.round.update_results_games(tournament)
            elif user_choice in ["3","3)"] :
                self.finish_tournament(tournament)
            elif user_choice in ["4","4)"] :
                break

        
    def finish_tournament(self, tournament) :

        while True :

            rounds = tournament.rounds
            current_round = tournament.current_round
            actual_round = rounds[current_round-1]

            if tournament.current_round < tournament.number_of_rounds :
                self.view.show_message(f"\nThis tournament should last {tournament.number_of_rounds} rounds\n1) Finish the tournament earlier \n2) Back \n")
                user_choice = int(self.view.get_input("\nSelect an option : "))
                if user_choice == 1 :
                    continue
                elif user_choice == 1 :
                    break
            if actual_round.state == "in_progress" :
                self.view.show_message(f"\nPlease update the last round results before to finish the tournament")
                break
            elif actual_round.state == "finished" :
                self.view.show_message(f"\nWARNING : The tournament will no longer be modifiable . Do you want to finish the tournament ?\n1) Finish the tournament anyway \n2) Back\n")
                user_choice = int(self.view.get_input("\nSelect an option : "))
                if user_choice == 1 :
                    tournament.state = "finished"
                    tournament.save_json()
                    self.view.show_message(f"\nThe tournament is now finish. You can view the reports on the menu \"Tournament reports\" ")
                    break
                elif user_choice == 2 :
                    break





    def _select_tournament(self) :
        """Show the list of all tournaments and the user select
        Return the tournament object selected """

        while True:
            tournaments = Tournament.deserialize_all_tournaments()
            self.view.show_tournaments_list(tournaments)
            user_input = self.view.get_input("\nSelect a tournament : ")

            if int(user_input) > len(tournaments):
                self.view.show_message("No tournament was find with that ID. Please try again.")
            else:
                tournament_index = int(user_input)-1
                tournament = tournaments[tournament_index]
                if tournament.state == "finished" :
                    self.view.show_message(f"\nThis tournament is finished. You can view the reports on the menu \"Tournament reports\" ")
                    break
                else :
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

        while True :
            rounds = tournament.rounds
            current_round = tournament.current_round
            if len(rounds) > 0 :
                actual_round = rounds[current_round-1]
                if actual_round.state == "in_progress" :
                    self.view.show_message("Please update the current round before to create a new one")
                    break
    
            round = self.generate_round(tournament)
            self.view.show_games_list(round)
            tournament.rounds.append(round)
            tournament.current_round += 1
            tournament.state = "in progress"
            tournament.save_json()
            break
 

    def generate_round(self, tournament) :

        games_list = []
        players = tournament.get_players_sorted()
        while players :

            for player in players :
                players.remove(player)
                previous_opponents = tournament.get_previous_opponents(player)
                if len(players) > len(previous_opponents) :
                    players = [player for player in players if player not in previous_opponents]
                opponent = players[0]
                players.remove(opponent)
                game = Game(player, opponent)
                games_list.append(game)
                break

        round = Round(f"ROUND {tournament.current_round+1}", games_list, "in_progress" )    
        return round

    def update_results_games(self, tournament):
    
        while True :
            rounds = tournament.rounds
            current_round = tournament.current_round

            if len(rounds) == 0 :
                self.view.show_message("Please create a round before to update")
                break
            else :
                actual_round = rounds[current_round-1]
                if actual_round.state == "finished" :
                    self.view.show_message("The round is already updated, please create a new one")
                    break
                elif actual_round.state == "in_progress" :
                    for game in actual_round.games_list :
                        winner = self.view.update_game_result(game)
                        if winner == game.player1 :
                                game.player1.score +=1
                        elif winner == game.player2 :
                                game.player2.score +=1
                        elif winner == None :
                            game.player1.score +=0.5
                            game.player2.score +=0.5

                    actual_round.state = "finished"
                    tournament.save_json()
                    break