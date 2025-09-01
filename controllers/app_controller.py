from models import *
from views import *
from rich import print
from .players_controller import PlayersController
from .tournaments_controller import TournamentsController
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
        self.view.main_menu()
        input_live = self.view.get_input("\nChoose an option : ")

        if input_live == "1" or input_live == "1)":
            self.manage_tournaments()    
        elif input_live == "2" or input_live == "2)" :
            self.manage_players()
        elif input_live == "3" or input_live == "3)" :
            pass
        elif input_live == "4" or input_live == "4)" :
            sys.exit()
        else :
            self.view.show_message("Erreur veuilez réessayer")
            self.run()

    def manage_tournaments(self):
        """
        Display the tournament management menu, collect the user selection and delegates tasks to the TournamentsController
        for creating tournaments, adding players, playing tournaments, or go back.
        """
        self.view.manage_tournaments_menu()
        input_live = self.view.get_input("\nChoose an option : ")
        while input_live == "1" or input_live == "1)": 
            TournamentsController(self).create()
        while input_live == "2" or input_live == "2)":
            TournamentsController(self).add_player_tournament()
        while input_live == "3" or input_live == "3)":
            pass
        while input_live == "4" or input_live == "4)":   
            self.run()

    def manage_players(self):
        """
        Display the player management menu, collect the user selection and delegates tasks to the PlayersController for
        listing or adding players, or go back.
        """
        
        self.view.manage_players_menu()
        input_manageplayers = self.view.get_input("\nChoose an option : ")
        while input_manageplayers == "1" or input_manageplayers == "1)" :
            PlayersController(self).players_list()
            self.manage_players()
        while input_manageplayers == "2" or input_manageplayers == "2)" :
            PlayersController(self).add_player()
            self.manage_players()
        while input_manageplayers == "3" or input_manageplayers == "3)" :
            self.run()



    

    

