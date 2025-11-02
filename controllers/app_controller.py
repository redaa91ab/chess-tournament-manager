from views import View
from .players_controller import PlayersController
from .tournaments_controller import TournamentsController
from rich import print

class AppController:
    """
    A controller class for managing the main application.
    It handles and display the main menu and delegates tasks to
    other controllers.
    """

    def __init__(self):
        """
        Initialize a AppController instance.

        Creates a View instance for display and input
        """
        self.view = View()
        self.players = PlayersController(self.view)
        self.tournament = TournamentsController(self.view)


    def run(self):
        """
        Run the main application.

        Displays the main menu, collect user input, and directs the user to
        manage tournaments, players, reports, or exit.
        """

        while True :
            self.view.show_main_menu()
            user_choice = self.view.get_input("\nChoose an option : ")

            if user_choice in ["1", "1)"] :
                self.tournament.manage_tournaments()    
            elif user_choice in ["2", "2)"] :
                self.manage_players()
            elif user_choice in ["3", "3)"] :
                pass
            elif user_choice in ["4", "4)"]:
                break
            else :
                self.view.show_message("Please an option between 1 and 4.")


    def manage_players(self):
        """
        Display the player management menu, collect the user selection and delegates tasks to the PlayersController for
        listing or adding players, or go back.
        """
        while True :
            self.view.show_manage_players_menu()
            user_choice = self.view.get_input("\nChoose an option : ")
            if user_choice == "1" or user_choice == "1)":
                self.players.display_all_players()
            elif user_choice == "2" or user_choice == "2)":
                self.players.add_player()
            elif user_choice == "3" or user_choice == "3)":
                break



    

    

