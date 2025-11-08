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
                self.players.manage_players()
            elif user_choice in ["3", "3)"] :
                self.tournament.reports_menu()
            elif user_choice in ["4", "4)"]:
                break
            else :
                self.view.show_message("Please choose an option between 1 and 4.")



    

    

