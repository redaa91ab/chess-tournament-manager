from views import View
from .players_controller import PlayersController
from .tournaments_controller import TournamentsController
from rich import print
import sys

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

    def run(self):
        """
        Run the main application.

        Displays the main menu, collect user input, and directs the user to
        manage tournaments, players, reports, or exit.
        """
        self.view.show_main_menu()
        user_choice = self.view.get_input("\nChoose an option : ")

        if user_choice == "1" or user_choice == "1)":
            self.manage_tournaments()    
        elif user_choice == "2" or user_choice == "2)":
            self.manage_players()
        elif user_choice == "3" or user_choice == "3)":
            pass
        elif user_choice == "4" or user_choice == "4)":
            sys.exit()
        else :
            self.view.show_message("Erreur veuilez réessayer")
            self.run()

    def manage_tournaments(self):
        """
        Display the tournament management menu, collect the user selection and delegates tasks to the TournamentsController
        for creating tournaments, adding players, playing tournaments, or go back.
        """
        self.view.show_tournaments_menu()
        user_choice = self.view.get_input("\nChoose an option : ")
        while user_choice == "1" or user_choice == "1)": 
            TournamentsController(self).create()
        while user_choice == "2" or user_choice == "2)":
            TournamentsController(self).add_player_tournament()
        while user_choice == "3" or user_choice == "3)":
            pass
        while user_choice == "4" or user_choice == "4)":   
            self.run()

    def manage_players(self):
        """
        Display the player management menu, collect the user selection and delegates tasks to the PlayersController for
        listing or adding players, or go back.
        """

        self.view.show_manage_players_menu()
        user_choice = self.view.get_input("\nChoose an option : ")
        while user_choice == "1" or user_choice == "1)":
            PlayersController(self).display_all_players()
            self.manage_players()
        while user_choice == "2" or user_choice == "2)":
            PlayersController(self).add_player()
            self.manage_players()
        while user_choice == "3" or user_choice == "3)":
            self.run()



    

    

