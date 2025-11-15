from models import Tournament, Player, Round, Game, PlayerTournament
from .players_controller import PlayersController
from datetime import datetime


class TournamentsController:
    """
    A controller class for managing tournament.
    It provides methods to create, select or modify a tournament
    """

    def __init__(self, view):
        """
        Initialize a TournamentsController instance.

        Args:
            view: An instance of the View class
            players_controller : An instance of the Players Controller
            round_controller : An instance of the Round Controller
        """
        self.view = view
        self.players_controller = PlayersController(self.view)
        self.round_controller = RoundController(self.view)

    def manage_tournaments(self):
        """
        Display the tournament management menu and offer 4 option : 
        create tournament, add players, start tournament, or going back.
        """

        while True :
            self.view.show_tournaments_menu()
            user_choice = self._get_valid_choice(4)
            if user_choice == 1 :
                self.create()
            elif user_choice == 2 :
                tournament = self._select_tournament()
                if tournament :
                    if tournament.state == "finished" :
                        self.view.show_message("This tournament is finished. You can't add players.")
                    else :
                        self.add_player_tournament(tournament)
            elif user_choice == 3:
                tournament = self._select_tournament()
                if tournament :
                    if tournament.state == "finished" :
                        self.view.show_message("This tournament is finished. You can't start a tournament.")
                    elif len(tournament.players) < 4 :
                        self.view.show_message(f"You need at least 4 players to start a tournament.  Current number of players = {len(tournament.players)}")
                    elif len(tournament.players) %2 != 0 :
                        self.view.show_message(f"You need a even number of players to start. Current number of players = {len(tournament.players)}")
                    else :
                        self.start_tournament(tournament)
            elif user_choice == 4 : 
                break

    def create(self):
        """
        Create a tournament object and save it to JSON
        """
        self.view.show_message("\n[bold green]Create tournament[/bold green]\n")
        self.view.show_message("Enter the new tournament details below : ")
        tournament_name = self.view.get_input("Tournament name : ")
        place = self.view.get_input("Place : ")
        start_date = self._get_valid_date("Start date (DD/MM/YYYY) : ")
        end_date = self._get_valid_date("End date (DD/MM/YYYY) : ")
        number_of_rounds = self._get_valid_number_of_rounds()
        tournament = Tournament(tournament_name, place, start_date, end_date, number_of_rounds)
        tournament.save_json()


    def add_player_tournament(self, tournament) :
        """ Ask for national_chess_id, retrieve the player and create a PlayerTournament object then save it in players in the tournament"""

        while True : 
            national_chess_id = self.players_controller._get_valid_national_chess_id()
            player = Player.deserialize(national_chess_id)
            if player is None:
                self.view.show_message("\nThis player is not in the database :\n1) Type again \n2) Create a new player \n")
                user_choice = self._get_valid_choice(2)
                if user_choice == 1:
                    continue
                elif user_choice == 2:
                    player = self.players_controller.add_player(national_chess_id)
                    tournament.players.append(PlayerTournament(player, 0.0))
                    tournament.save_json()
                    self.view.show_message(f"\n{player.name} {player.surname} ({player.national_chess_id}) was successfully added to the tournament !")
                    break
            elif player :
                player_nid = player.national_chess_id
                nid_players_tournament = [player.player.national_chess_id for player in tournament.players]
                if player_nid in nid_players_tournament :
                    self.view.show_message(f"\n{player.name} {player.surname} ({player.national_chess_id}) is already saved in the tournament.")
                    break
                else :
                    tournament.players.append(PlayerTournament(player, 0.0))
                    tournament.save_json()
                    self.view.show_message(f"\n{player.name} {player.surname} ({player.national_chess_id}) was successfully added to the tournament !")
                    break
                

    def start_tournament(self, tournament):
        """ Display start_tournament menu, then either create a new round, update the actual round or finish the tournament"""

        while True :
            self.view.show_start_tournament_menu()
            user_choice = self._get_valid_choice(4)
            if user_choice == 1 :
                self.round_controller.create_round_menu(tournament)
            elif user_choice == 2 :
                self.round_controller.update_results_games(tournament)
            elif user_choice == 3:
                self.finish_tournament(tournament)
            elif user_choice == 4 :
                break

        
    def finish_tournament(self, tournament) :
        """ D"""

        while True :
            rounds = tournament.rounds
            current_round = tournament.current_round
            actual_round = rounds[current_round-1]

            if actual_round.state == "in_progress" :
                self.view.show_message(f"\nPlease update the last round results before to finish the tournament")
                break

            elif tournament.current_round < tournament.number_of_rounds :
                self.view.show_message(f"\nThis tournament should last {tournament.number_of_rounds} rounds"
                                        "\n1) Finish the tournament earlier"
                                        "\n2)[red] Back [/red] \n"
                                        )
                user_choice = self._get_valid_choice(2)
                if user_choice == 1 :
                    pass
                elif user_choice == 2 :
                    break

            else :
                tournament.state = "finished"
                tournament.save_json()
                self.view.display_rank_players(tournament)
                self.view.show_message(f"\n Tournament officialy finish. You can view the rank above")
   


    def reports_menu(self) :
        while True :
            self.view.reports_menu()
            user_choice = self._get_valid_choice(2)
            if user_choice == 1 :
                self.players_controller.display_all_players()
            elif user_choice == 2 :
                self.reports_tournaments()
            elif user_choice == 3 :
                break


    def reports_tournaments(self) :
        while True :
            tournament = self._select_tournament()
            if tournament :
                self.report_tournament(tournament)
            else :
                break

    def report_tournament(self, tournament):
        while True :
            self.view.reports_tournament_menu()
            user_choice = self._get_valid_choice(3)
            if user_choice == 1 :
                self.view.display_players_tournament(tournament)
            elif user_choice == 2 :
                self.view.display_tournament_rounds(tournament)
                self.view.display_rank_players(tournament)
            elif user_choice == 3 :
                break


    def _select_tournament(self) :
        """Show the list of all tournaments and the user select
        Return the tournament object selected """

        while True:
            tournaments = Tournament.deserialize_all_tournaments()
            self.view.show_select_tournament(tournaments)
            user_choice = self._get_valid_choice(len(tournaments)+1)

            if user_choice == len(tournaments)+1:
                break
            else:
                tournament_index = user_choice-1
                tournament = tournaments[tournament_index]
                return tournament
            
    def _get_valid_choice(self, number_of_choice) :
        while True :
            try :
                user_choice = int(self.view.get_input("Select an option : "))
                if 1 <= user_choice <= number_of_choice :
                    return user_choice
                else :
                    self.view.show_message("Please select a valid option")
            except ValueError:
                self.view.show_message("Please enter a number")
            
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
    """
    A controller class for managing rounds.
    It provides methods to create or update rounds
    """
    
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
            if tournament.state == "finished" :
                self.view.show_message("The tournament is finished. You can't create a new round)")
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
                game = Game(player, 0.0, opponent, 0.0)
                games_list.append(game)
                break

        start_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        round = Round(f"ROUND {tournament.current_round+1}", games_list, "in_progress", start_date )    
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
                                game.player1_score =1
                                game.player1.total_score +=1
                        elif winner == game.player2 :
                                game.player2_score =1
                                game.player2.total_score +=1
                        elif winner == None :
                            game.player1_score =0.5
                            game.player1.total_score +=0.5
                            game.player2_score =0.5
                            game.player2.total_score +=0.5

                    end_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    actual_round.end_date = end_date
                    actual_round.state = "finished"
                    if current_round == tournament.number_of_rounds :
                        TournamentsController(self.view).finish_tournament(tournament)
                    tournament.save_json()
                    break