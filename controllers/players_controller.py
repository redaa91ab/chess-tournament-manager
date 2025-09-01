from models import *
from views import *
from rich import print


class PlayersController: 
    """
    A controller class for managing player. 
    It provides methods to display all the players and adding new players to the database
    """
    def __init__(self, parent):
        """
        Initialize a PlayersController instance.

        Args:
            parent: app_controller.py
        """
        self.view = View()
        self.parent = parent

    def players_list(self):
        """
        Display the list of all players using the method return_players of the Player model.
        """
        self.view.show_message(Player.return_players())

    def add_player(self) :
        """ 
        Collect the player details, then use the methods save_json of the Player model.
        """

        self.view.show_message("\nEnter the new player details below :")
        id = self.view.get_input("National chess ID : ")
        current_player = Player.return_player_details(id)
        if current_player :
            self.view.show_message("This player already exist")
        elif current_player == None :
            name = self.view.get_input("Name : ")
            surname = self.view.get_input("Surname : ")
            birthdate = self.view.get_input("Birthdate :")
            self.view.show_message("\nPlayer successfully added !")
            player = Player(id, name, surname, birthdate)
            player.save_json()
