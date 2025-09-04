from models import Tournament, Player
from rich import print


class TournamentsController:
    """
    A controller class for managing tournament.
    It provides methods to create a new tournament in tournaments.json and add new players to a tournament
    """

    def __init__(self,view, parent = None):
        """
        Initialize a TournamentsController instance.

        Args:
            view: An instance of the View class
            parent : app_controller.py
        """
        self.parent = parent
        self.view = view

    def create(self):
        """
        Collect new tournament details and save it in tournaments.json by using the methods save_json of the model Tournament
        """
        self.view.show_message("\n[bold green]New tournament[/bold green]\n")
        self.view.show_message("Enter the new tournament details below : ")
        tournament_name = self.view.get_input("Tournament name : ")
        place = self.view.get_input("Place : ")
        start_date = self.view.get_input("Start date (DD/MM/YYYY) : ")
        end_date = self.view.get_input("End date (DD/MM/YYYY): ")
        number_of_rounds = self.view.get_input("Number of rounds : ")

        try:
            number_of_rounds = int(number_of_rounds)
            if number_of_rounds <= 0:
                raise ValueError("Number of rounds must be positive")
            from datetime import datetime
            datetime.strptime(start_date, "%d/%m/%Y")
            datetime.strptime(end_date, "%d/%m/%Y")
        except ValueError as e:
            self.view.show_message(f"Invalid input: {e}")
            return

        tournament = Tournament(tournament_name, place, start_date, end_date, number_of_rounds)
        tournament.save_json()
        self.add_player_tournament(tournament_name)

    def add_player_tournament(self, tournament_name = None):
        """
        Add players to a tournament in tournaments.json

        Args:
            tournament_name : The name of the tournament to add players to.
                              If None, prompts the user to enter a tournament name.

        Collect the tournament name if not provided and add player to the tournament in tournaments.json.
        If a player doesn't exist, offers the option to create a new player or try again.
        """
        while tournament_name == None :
            user_input = self.view.get_input("\nEnter the tournament name : ") 
            if Tournament.get_tournament_details(user_input) == None :
                self.view.show_message("We didn't find any match, please try again")
            else :
                tournament_name = user_input

        self.view.show_message(f"[bold green]\n{tournament_name}[/bold green]")
        self.view.show_add_players_tournament_menu()
        user_choice = self.view.get_input("\nChoose an option : ")

        while user_choice == "1" or user_choice == "1)":
            self.view.show_message(f"\n[bold green]\n{tournament_name}[/bold green]\n")
            national_chess_id = self.view.get_input("Add a player (National Chess ID) : ")
            add_player = Player.get_player_details(national_chess_id)
            if add_player == None :
                self.view.show_message("\nThis player doesn't exist :\n1) Try again \n2) Create a new player \n")
                user_choice_option = self.view.get_input("Choose an option : ")
                if user_choice_option == "1" or user_choice_option == "1)":
                    pass
                elif user_choice_option == "2" or user_choice_option == "2)":
                    name = self.view.get_input("Name : ")
                    surname = self.view.get_input("Surname : ")
                    birthdate = self.view.get_input("Birthdate : ")
                    Player(national_chess_id, name, surname, birthdate).save_json()
                    Tournament.add_player(tournament_name, national_chess_id)
                    self.view.show_message(f"\n{name} {surname} ({national_chess_id}) was successfully added !")
                    self.add_player_tournament(tournament_name)
            else :
                Tournament.add_player(tournament_name, national_chess_id)
                self.view.show_message(f"\n{add_player[1]} {add_player[2]} ({add_player[0]}) was successfully added !")
                self.add_player_tournament(tournament_name)

        while user_choice == "2" or user_choice == "2)":
            self.parent.manage_tournaments()



