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

        args :
            self.view : View instance for display and input
            self.players : PlayersController instance, for handling players menu
            self. TournamentsController instance, for handling tournaments menu

        """
        self.view = View()
        self.players = PlayersController(self.view)
        self.tournament = TournamentsController(self.view)

    def run(self):
        """
        Run the main application.

        Displays the main menu and directs the user to
        manage tournaments, players, reports, or exit.
        """

        while True :
            self.view.show_main_menu()
            user_choice = self.tournament.get_valid_choice(4)

            if user_choice == 1 :
                self.tournament.manage_tournaments()    
            elif user_choice == 2 :
                self.players.manage_players()
            elif user_choice == 3 :
                self.tournament.reports_menu()
            elif user_choice == 4 :
                break


    

    

